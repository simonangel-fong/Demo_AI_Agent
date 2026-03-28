import asyncio
import uuid
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel

from agent.agent import Agent 

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(title="Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Session store
# ---------------------------------------------------------------------------

SESSION_TTL_SECONDS = 60 * 60  # 1 hour


class SessionEntry:
    def __init__(self):
        self.agent = Agent()
        self.last_active = time.time()

    def touch(self):
        self.last_active = time.time()

    def is_expired(self) -> bool:
        return time.time() - self.last_active > SESSION_TTL_SECONDS


_sessions: dict[str, SessionEntry] = {}


def get_or_create_session(session_id: str) -> SessionEntry:
    if session_id not in _sessions:
        _sessions[session_id] = SessionEntry()
    entry = _sessions[session_id]
    entry.touch()
    return entry


async def cleanup_expired_sessions():
    """Background task — purge sessions idle longer than SESSION_TTL_SECONDS."""
    while True:
        await asyncio.sleep(60 * 10)  # run every 10 minutes
        expired = [sid for sid, entry in _sessions.items()
                   if entry.is_expired()]
        for sid in expired:
            del _sessions[sid]


@app.on_event("startup")
async def startup():
    asyncio.create_task(cleanup_expired_sessions())


# ---------------------------------------------------------------------------
# Static routes
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    return FileResponse("templates/index.html")


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class NewSessionResponse(BaseModel):
    session_id: str


class ResetResponse(BaseModel):
    session_id: str
    status: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/sessions", response_model=NewSessionResponse)
async def create_session():
    """Create a new agent session and return its ID."""
    session_id = str(uuid.uuid4())
    _sessions[session_id] = SessionEntry()
    return NewSessionResponse(session_id=session_id)


@app.get("/sessions/{session_id}/run")
async def run_task(session_id: str, task: str):
    """
    Stream agent execution as Server-Sent Events.

    Each event is a JSON-encoded AgentEvent:
        data: {"type": "thinking"|"skill"|"command"|"output"|"complete"|"error", "content": "..."}

    Connect with:
        const es = new EventSource(`/sessions/${id}/run?task=...`)
        es.onmessage = e => console.log(JSON.parse(e.data))
    """
    entry = get_or_create_session(session_id)

    async def event_generator():
        # Run the blocking agent in a thread so we don't block the event loop
        loop = asyncio.get_event_loop()
        queue: asyncio.Queue = asyncio.Queue()

        def run_agent():
            try:
                for event in entry.agent.run(task):
                    loop.call_soon_threadsafe(queue.put_nowait, event)
            finally:
                loop.call_soon_threadsafe(queue.put_nowait, None)  # sentinel

        thread = asyncio.to_thread(run_agent)
        asyncio.create_task(thread)

        while True:
            event = await queue.get()
            if event is None:
                break
            yield f"data: {event.model_dump_json()}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # disable nginx buffering if behind proxy
        },
    )


@app.post("/sessions/{session_id}/reset", response_model=ResetResponse)
async def reset_session(session_id: str):
    """Clear the agent's conversation history without destroying the session."""
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    _sessions[session_id].agent.reset()
    _sessions[session_id].touch()
    return ResetResponse(session_id=session_id, status="reset")


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Destroy a session entirely."""
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    del _sessions[session_id]
    return {"status": "deleted"}
