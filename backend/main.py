# backend/main.py
from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import List, Dict

from backend.memory import build_checkpoint_store
from backend.graph import build_graph, GraphState

app = FastAPI(title="PCI LangGraph API")

graph = build_graph(build_checkpoint_store())


class Message(BaseModel):
    role: str
    content: str


class QueryRequest(BaseModel):
    messages: List[Message]


class QueryResponse(BaseModel):
    segment: str
    suggestion: str
    messages: List[Dict]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def handle_query(payload: QueryRequest, session_id: str = Header(...)):
    state: GraphState = {
        "messages": [m.model_dump() for m in payload.messages],
        "segment": "",
        "suggestion": "",
    }
    out = graph.invoke(state, config={"configurable": {"thread_id": session_id}})
    return QueryResponse(**out)
