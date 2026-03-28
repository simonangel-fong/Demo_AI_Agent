import os
import subprocess
import threading
from pathlib import Path
from typing import Generator
from dotenv import load_dotenv
from anthropic import Anthropic

from .events import AgentEvent

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-5")

AGENT_DIR = Path(__file__).parent          # project/agent/
AGENT_MD  = AGENT_DIR / "AGENT.md"
SKILLS_DIR = AGENT_DIR / "skills"
TOOLS_DIR  = AGENT_DIR / "tools"
EXPORTS_DIR = AGENT_DIR / "exports"

with open(AGENT_MD, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# Safety limits
COMMAND_TIMEOUT_SECONDS = 30
MAX_CONTEXT_MESSAGES = 40


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

class Agent:
    """
    Persistent conversational agent designed to be called from FastAPI.

    One Agent instance lives per user session. The `context` list accumulates
    across multiple `run()` calls so the agent remembers previous tasks.

    Usage (inside FastAPI SSE endpoint):
        agent = Agent()
        for event in agent.run("summarise https://example.com"):
            yield f"data: {event.model_dump_json()}\\n\\n"
    """

    def __init__(self) -> None:
        self._client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self._context: list[dict] = []
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, task: str) -> Generator[AgentEvent, None, None]:
        """
        Execute a task and yield AgentEvents in real time.
        Blocking — wrap with asyncio.to_thread() in FastAPI.
        """
        if not self._lock.acquire(blocking=False):
            yield AgentEvent(
                type="error",
                content="Agent is already running a task. Please wait.",
            )
            return

        try:
            self._append_user(task)
            yield from self._agent_loop()
        except Exception as exc:
            yield AgentEvent(type="error", content=f"Unexpected error: {exc}")
        finally:
            self._lock.release()

    def reset(self) -> None:
        """Clear conversation history (start a new session)."""
        with self._lock:
            self._context.clear()

    # ------------------------------------------------------------------
    # Core agentic loop
    # ------------------------------------------------------------------

    def _agent_loop(self) -> Generator[AgentEvent, None, None]:
        while True:
            llm_output = self._call_llm()

            yield AgentEvent(type="thinking", content=llm_output)
            self._append_assistant(llm_output)

            if llm_output.startswith("complete:"):
                answer = llm_output.split("complete:", 1)[1].strip()
                yield AgentEvent(type="complete", content=answer)
                break

            elif llm_output.startswith("skill:"):
                skill_cmd = llm_output.split("skill:", 1)[1].strip()
                yield AgentEvent(type="skill", content=skill_cmd)
                result = self._execute(skill_cmd)
                yield AgentEvent(type="output", content=result)
                self._append_user(f"command execution: {result}")

            elif llm_output.startswith("command:"):
                exec_cmd = llm_output.split("command:", 1)[1].strip()
                yield AgentEvent(type="command", content=exec_cmd)
                result = self._execute(exec_cmd)
                yield AgentEvent(type="output", content=result)
                self._append_user(f"command execution: {result}")

            else:
                self._append_user("Please follow the output format.")

    # ------------------------------------------------------------------
    # LLM call
    # ------------------------------------------------------------------

    def _call_llm(self) -> str:
        response = self._client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=self._context,
        )
        return response.content[0].text.strip()

    # ------------------------------------------------------------------
    # Command execution (sandboxed to AGENT_DIR)
    # ------------------------------------------------------------------

    def _execute(self, command: str) -> str:
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=AGENT_DIR,
                timeout=COMMAND_TIMEOUT_SECONDS,
            )
            output = result.stdout + result.stderr
            return output if output.strip() else "(no output)"
        except subprocess.TimeoutExpired:
            return f"Error: command timed out after {COMMAND_TIMEOUT_SECONDS}s"
        except Exception as exc:
            return f"Error executing command: {exc}"

    # ------------------------------------------------------------------
    # Context management
    # ------------------------------------------------------------------

    def _append_user(self, content: str) -> None:
        self._context.append({"role": "user", "content": content})
        self._trim_context()

    def _append_assistant(self, content: str) -> None:
        self._context.append({"role": "assistant", "content": content})
        self._trim_context()

    def _trim_context(self) -> None:
        """
        Keep context under MAX_CONTEXT_MESSAGES by dropping oldest pairs.
        Always preserves the first message (original task anchor).
        """
        if len(self._context) > MAX_CONTEXT_MESSAGES:
            self._context = [self._context[0]] + self._context[3:]