from typing import Literal
from pydantic import BaseModel


class AgentEvent(BaseModel):
    """
    Typed SSE event emitted by the agent.

    type        | meaning
    ------------|--------------------------------------------------
    thinking    | raw LLM output before it is classified
    skill       | agent is loading a skill (shell command)
    command     | agent is executing a shell command
    output      | stdout / stderr result of a skill or command
    complete    | final answer — the task is done
    error       | any exception or unexpected state
    """
    type: Literal[
        "thinking",
        "skill",
        "command",
        "output",
        "complete",
        "error"
    ]
    content: str
