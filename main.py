"""
FastAPI Backend for the Medical KRR Chatbot
Wraps the existing query_handler.py pipeline (unchanged) with a REST API
so any frontend (not just Streamlit) can talk to it.

Run with:
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid

# --- reuse your existing pipeline as-is, no changes needed there ---
from query_handler import handle_query, ChatSession

app = FastAPI(title="Medical KRR Chatbot API", version="1.0")

# Allow the frontend (opened as a local file or served separately) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # tighten to your frontend's origin before deploying
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store: session_id -> ChatSession
sessions: Dict[str, ChatSession] = {}


class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    intent: str
    response: str
    krr_data: Dict[str, Any]


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    session_id = req.session_id or str(uuid.uuid4())
    session = sessions.setdefault(session_id, ChatSession())

    intent, response, krr_data = handle_query(
        query=req.query,
        chat_history=session.get_history()
    )

    session.add_message("user", req.query)
    session.add_message("assistant", response)

    return ChatResponse(
        session_id=session_id,
        intent=intent,
        response=response,
        krr_data=krr_data or {}
    )


@app.post("/reset/{session_id}")
def reset(session_id: str):
    sessions.pop(session_id, None)
    return {"status": "cleared"}


@app.get("/health")
def health():
    return {"status": "ok"}
