# backend/graph.py
from typing import TypedDict, List, Dict

from langgraph.graph import StateGraph

from backend.segmentation import segment_customer
from backend.suggestion import generate_suggestion


class GraphState(TypedDict):
    messages: List[Dict[str, str]]
    segment: str
    suggestion: str


# Node 1 — pass context through
def node_context(state: GraphState, **_) -> GraphState:
    return state


# Node 2 — assign customer segment
def node_segment(state: GraphState, **_) -> GraphState:
    state["segment"] = segment_customer(state["messages"][-1]["content"])
    return state


# Node 3 — generate suggestion
def node_suggest(state: GraphState, **_) -> GraphState:
    q = state["messages"][-1]["content"]
    seg = state["segment"]
    ans = generate_suggestion(seg, q)

    state["suggestion"] = ans
    state["messages"].append({"role": "assistant", "content": ans})
    return state


def build_graph(checkpointer):
    g = StateGraph(GraphState)
    g.add_node("context", node_context)
    g.add_node("segment", node_segment)
    g.add_node("suggest", node_suggest)

    g.set_entry_point("context")
    g.add_edge("context", "segment")
    g.add_edge("segment", "suggest")
    g.set_finish_point("suggest")

    return g.compile(checkpointer=checkpointer)
