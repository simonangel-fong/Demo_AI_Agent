# Agent Evolution: From LLM Call to Agent System

> A progressive demonstration of AI agent development, from a single LLM API call to an agent system.

- [Agent Evolution: From LLM Call to Agent System](#agent-evolution-from-llm-call-to-agent-system)
  - [What an AI Agent Actually Is](#what-an-ai-agent-actually-is)
  - [From Hype to Reality](#from-hype-to-reality)
  - [Evolution](#evolution)
    - [Stage 1 — LLM API Call](#stage-1--llm-api-call)
    - [Stage 2 — Terminal Input](#stage-2--terminal-input)
    - [Stage 3 — Conversation Memory](#stage-3--conversation-memory)
    - [Stage 4 — System \& User Prompts](#stage-4--system--user-prompts)
    - [Stage 5 — Tool Calling](#stage-5--tool-calling)
    - [Stage 6 — Packages as Skills](#stage-6--packages-as-skills)
    - [Stage 7 — Web UI \& Containerize](#stage-7--web-ui--containerize)

---

## What an AI Agent Actually Is

An `AI agent` is just a **loop** — the core logic fits in ~10 lines. Every layer on top is existing technology, nothing new.

**Core loop:**

```py
def main() -> None:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)                         # 1. Initialize API
    context = []                                                          # 2. Initialize memory
    while True:                                                           # 3. Interaction loop
        user_input = input("\n>> User Input:\n")                          # 4.   Get user input
        context.append({"role": "user", "content": user_input})           # 5.   Append user input to history
        while True:                                                       # 6.   Execution loop
            response = client.messages.create()                           # 7.     Call LLM API
            llm_output = response.content                                 # 8.     Get output
            context.append({"role": "assistant", "content": llm_output})  # 9.     Append LLM output to history
            if llm_output.startswith("complete:"):                        # 10.    Done → break
                break
            elif llm_output.startswith("command:"):                       # 11.    Tool call → execute
                pass
```

## From Hype to Reality

`AI` and `agentic systems` are powerful, but they follow familiar patterns in computing history — and understanding that distinction is what separates hype from sustainable value.

Just as `relational databases` unlocked business value through structured interaction via `SQL`, `LLMs` require well-designed `prompts` and `context` to be effective. The progression from a simple `API call` to an `AI agent` demonstrates that most underlying technologies already exist. The real innovation lies in how they are integrated and applied.

`LLMs` do not replace `computer science` fundamentals or engineering roles — they amplify them. **Strong system design, infrastructure, and operational practices** remain essential to turning AI capabilities into real, measurable business value.

At its core, the interaction model is unchanged: `input → process → output`. And as with any system, `garbage in means garbage out`. Poor inputs or unsafe instructions lead to unintended consequences. Just as an incorrect `SQL DELETE` can damage a database, an unsafe prompt or misconfigured agent introduces real operational risk.

---

## Evolution

Each stage introduces one concept required to move from a simple `LLM call` to an `agent system`.

The focus is not on features, but on how the loop evolves.

| stage | Name                  | Existing Technology     |
| ----- | --------------------- | ----------------------- |
| 1     | LLM API Call          | API request             |
| 2     | Prompt in Terminal    | `while` loop            |
| 3     | Memory via Context    | Array                   |
| 4     | System & User Prompts | String formatting       |
| 5     | Tool Calling          | CLI command             |
| 6     | Packages as Skills    | File system I/O         |
| 7     | Web UI & protable     | FastAPI + HTML + Docker |

---

### Stage 1 — LLM API Call

Send a prompt to an LLM via a single API request and print the response.

> Limitation: One-time request with a hardcoded prompt

```
prompt ──► LLM API ──► response
```

---

### Stage 2 — Terminal Input

**Goal:**  
Accept user input from the terminal and send it to the LLM.

**Diagram:**

```
user input ──► LLM API ──► response
     ▲                         │
     └─────────────────────────┘
```

**Limitation:**  
No memory — each input is a fresh API call with no conversation history.

---

### Stage 3 — Conversation Memory

**Goal:**  
Save conversation history by sending the full context on every API request.

**Diagram:**

```
user input ──► [ history + new input ] ──► LLM API ──► response
                        ▲                                  │
                        └──────────────────────────────────┘
```

**Limitation:**  
Response depends on prompt without persistent format.

---

### Stage 4 — System & User Prompts

**Goal:**  
Control LLM behavior and output format via a dedicated system prompt.

**Diagram:**

```
user input ──► [ system prompt + history + new input ] ──► LLM API ──► response
                                ▲                                          │
                                └──────────────────────────────────────────┘
```

**Limitation:**  
Outputs text only — the LLM cannot call tools or take actions.

---

### Stage 5 — Tool Calling

**Goal:**  
Enable the LLM to interact with the external world by calling tools.

**Diagram:**

```
user input ──► [ system prompt + history + new input ] ──► LLM API ───┬──► text ─────────────┐
                               ▲                                      │                      │
                               │                                      └──► tool call         │
                               │                                               │             │
                               │                                          CLI tool           │
                               │                                               │             │
                               └───────────────────────────────────────────────┴─────────────┘
```

**Limitation:**  
System prompt is hardcoded in the program — behavior cannot be changed without modifying the source code.

---

### Stage 6 — Packages as Skills

**Goal:**  
Shift from hardcoded behavior to configuration-driven behavior via external files.

**Diagram:**

```
user input ────► [ system.md + history + new input ] ─────────────► LLM API ───────────────────────┐
                                  ▲                                                                │
                                  ├───────────────────────────────────────────────── text ─────────┘
                                  │                                                                │
                                  ├───── read skills.md <──┬─── CLI tool <───── tool call ─────────┘
                                  │                        │
                                  └────── CLI ouput <──────┘
```

**Limitation:**  
UI is terminal-only — unfriendly for non-technical users.

---

### Stage 7 — Web UI & Containerize

**Goal:**  
Decouple interaction from execution by exposing the agent through a web interface.
Portable via Docker.

**Diagram:**

```
                  │ Containerize[Docker]                                                              │
                  │                                                                                   │
User input ──► Web UI ──► [ system.md + history + new input ] ─────────► LLM API ───────────────────┐ │
                  │                         ▲                                                       │ │
                  │                         ├────────────────────────────── text ───────────────────┘ │
                  │                         │                                                       │ │
                  │                         ├───── read skills.md <──┬─── CLI tool <─── tool call───┘ │
                  │                         │                        │                                │
                  │                         └────── CLI output <─────┘                                │
```

---
