"""
FastAPI REST API for the ShopEasy E-Commerce FAQ Bot.

Endpoints:
  POST /ask          — multi-turn FAQ question
  GET  /health       — liveness probe
  POST /reset/{tid}  — get a fresh thread_id

Run:
  uvicorn ecommerce_bot.api.main:app --reload --port 8001
"""

import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import agent  # noqa: F401 — ensures KB is built at startup
from agent import ask as _ask

app = FastAPI(
    title="ShopEasy E-Commerce FAQ Bot API",
    version="1.0.0",
    description="Agentic AI capstone — LangGraph + ChromaDB + Groq",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str
    thread_id: Optional[str] = None


class AskResponse(BaseModel):
    thread_id: str
    answer: str
    route: str
    faithfulness: float
    sources: list[str]


@app.get("/health")
def health():
    return {"status": "ok", "service": "ShopEasy E-Commerce FAQ Bot"}


@app.post("/ask", response_model=AskResponse)
def ask_endpoint(body: AskRequest):
    if not body.question.strip():
        raise HTTPException(status_code=422, detail="question must not be empty")

    thread_id = body.thread_id or str(uuid.uuid4())

    try:
        result = _ask(question=body.question, thread_id=thread_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return AskResponse(
        thread_id=thread_id,
        answer=result["answer"],
        route=result["route"],
        faithfulness=result["faithfulness"],
        sources=result["sources"],
    )


@app.post("/reset/{thread_id}")
def reset_thread(thread_id: str):
    new_id = str(uuid.uuid4())
    return {"message": "Use new_thread_id for your next request.", "new_thread_id": new_id}
