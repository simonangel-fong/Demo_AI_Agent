# Agent Evolution: From LLM Call to Agent System

> A progressive demonstration of AI agent development, from a single LLM API call to a multi-agent system. Each version introduces one new concept.  
> The goal is to show the _mental model evolution_, not the technical details.

- [Agent Evolution: From LLM Call to Agent System](#agent-evolution-from-llm-call-to-agent-system)
  - [Versions](#versions)
    - [v1 — LLM API call](#v1--llm-api-call)
    - [v2 — Prompt in Terminal](#v2--prompt-in-terminal)
    - [v3 — Memory via context](#v3--memory-via-context)
    - [v4 — System prompt and User Prompt](#v4--system-prompt-and-user-prompt)
    - [v5 — Tool Calling](#v5--tool-calling)
    - [v6 — Packages as Skills](#v6--packages-as-skills)
    - [v7 — Web UI](#v7--web-ui)
    - [v8 — Containerization](#v8--containerization)
  - [What's Deliberately Left Out](#whats-deliberately-left-out)
  - [Concept Map](#concept-map)
  - [Conclusion](#conclusion)

---

## Versions

### v1 — LLM API call

**Goal:** show that calling an LLM is just an API call — a skill any programmer already has.  
**What it does:** hardcoded prompt + API key → print response.  
**Demo:**

- `"What is the capital of France?"` hardcoded in the script.

---

### v2 — Prompt in Terminal

**Goal:** enable interactive usage.
**What it does:** terminal loop (`while True`) → input → API → output.
**Demo:**

- Stateless terminal chat(no memory).

---

### v3 — Memory via context

**Goal:** show the simplest possible memory implementation.  
**What it does:** `messages.append(message)` — the full conversation history is sent on every API call.  
**Demo:**

- ask `"what did I just say?"` and the agent answers correctly.

**Note:** RAG and other advanced memory techniques are out of scope here.

---

### v4 — System prompt and User Prompt

**Goal:** control behavior and output format.
**What it does:**

- separates system/user prompts; enforces structured output.

**Demo:**

- JSON-formatted responses.

---

### v5 — Tool Calling

**Goal:** show that an agent can act on the world, not just produce text. Demonstrate two flavours of tool use in one step.  
**What it does:**

- LLM triggers tools → executes → feeds result back.

**Demo A — built-in CLI tool:**

- `"What is today's date?"` → shell `date`

**Demo B — external function:**

- `"Weather in NYC"` → `get_nyc_weather.py`

**Key point:**

- unified tool abstraction regardless of execution source.

---

### v6 — Packages as Skills

**Goal:** sshift from code-driven to configuration-driven agents.
**What it does:**

- `system.md` → behavior definition
- `skills.md` → tool rules

**Demo:**

- Add skill → agent behavior changes without code updates.

**Key point:** mirrors real-world agent frameworks.

---

### v7 — Web UI

**Goal:** decouple interface from execution.
**What it does:**

- FastAPI backend
- Minimal chat UI

**Demo:**

- Same agent, now accessible via browser.

**Key point**: agent becomes a service.

---

### v8 — Containerization

**Goal:** make the agent portable, reproducible, and deployable.
**What it does:**

- Dockerize the full stack (agent + UI + dependencies)

**Demo:**

- Local: docker compose up → identical environment

**Key point:**
Containerization defines a runtime contract — same input, same output, any environment.

---

## What's Deliberately Left Out

| Topic                     | Reason                                           |
| ------------------------- | ------------------------------------------------ |
| RAG / vector memory       | Advanced memory — out of scope for v3            |
| Guardrails / security     | Intentionally deferred to highlight risk in v10  |
| Error handling / retries  | Implementation detail                            |
| MCP protocol              | Standardization not required for concept clarity |
| Multi-agent orchestration | Beyond scope; focus is single-agent evolution    |

---

## Concept Map

| Version | Phase                         | New concept introduced         |
| ------- | ----------------------------- | ------------------------------ |
| v1      | LLM API call                  | LLM as API call                |
| v2      | Prompt in Terminal            | Conversation loop              |
| v3      | Memory via context            | Context as memory              |
| v4      | System prompt and User Prompt | Behaviour shaping via prompts  |
| v5      | Tool Calling                  | Tool execution abstraction     |
| v6      | Packages as Skills            | File-based agent configuration |
| v7      | Web UI                        | Service interface (HTTP layer) |
| v8      | Containerization              | Portable, reproducible runtime |

---

_Each version is a standalone, runnable script. A reader should be able to check out any version and understand exactly what concept it introduces._

---

## Conclusion

`AI` and `agentic systems` are powerful, but they follow familiar patterns in computing history.

Like `relational databases`, which unlocked business value through structured interaction via `SQL`, `LLMs` require well-designed `prompts` and `context` to be effective. The progression in this project—from a simple API call to an EKS-based assistant agent—demonstrates that most underlying technologies already exist. The innovation lies in how they are integrated and applied.

`LLMs` **do not replace** computer science fundamentals or engineering roles. Instead, they amplify `LLMs` impact. **Strong system design, infrastructure, and operational practices remain essential** to turning AI capabilities into real business value.

At its core, the interaction model remains unchanged: `input → process → output`. As with any system, it follows the `principle of “garbage in, garbage out.”` Poor inputs or unsafe instructions can lead to unintended consequences. Just as an incorrect `SQL DELETE` statement can damage a database, an unsafe prompt or misconfigured agent can introduce real operational risk.

This project highlights both sides: the efficiency gains AI can bring, and the importance of applying it with engineering discipline and caution.
