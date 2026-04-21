"""
LangGraph StateGraph for the ShopEasy E-Commerce FAQ Bot.

Topology:
  START → memory → router ──[route_decision]──► retrieve → answer → eval ──[eval_decision]──► save → END
                                              ► skip    →         ↑                        ► answer (retry)
                                              ► tool    →         ↑
"""

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from ecommerce_bot.state import CapstoneState
from ecommerce_bot.nodes import (
    memory_node, router_node, retrieval_node, skip_retrieval_node,
    tool_node, answer_node, eval_node, save_node, MAX_EVAL_RETRIES,
)


def route_decision(state: CapstoneState) -> str:
    route = state.get("route", "retrieve")
    if route == "tool":   return "tool"
    if route == "skip":   return "skip"
    return "retrieve"


def eval_decision(state: CapstoneState) -> str:
    faithfulness  = state.get("faithfulness", 1.0)
    eval_retries  = state.get("eval_retries", 0)
    if faithfulness < 0.7 and eval_retries <= MAX_EVAL_RETRIES:
        return "answer"
    return "save"


def build_graph():
    graph = StateGraph(CapstoneState)

    graph.add_node("memory",   memory_node)
    graph.add_node("router",   router_node)
    graph.add_node("retrieve", retrieval_node)
    graph.add_node("skip",     skip_retrieval_node)
    graph.add_node("tool",     tool_node)
    graph.add_node("answer",   answer_node)
    graph.add_node("eval",     eval_node)
    graph.add_node("save",     save_node)

    graph.set_entry_point("memory")

    graph.add_edge("memory",   "router")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("skip",     "answer")
    graph.add_edge("tool",     "answer")
    graph.add_edge("answer",   "eval")
    graph.add_edge("save",     END)

    graph.add_conditional_edges(
        "router", route_decision,
        {"retrieve": "retrieve", "skip": "skip", "tool": "tool"},
    )
    graph.add_conditional_edges(
        "eval", eval_decision,
        {"answer": "answer", "save": "save"},
    )

    app = graph.compile(checkpointer=MemorySaver())
    print("Graph compiled successfully")
    return app


compiled_app = build_graph()
