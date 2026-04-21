"""CapstoneState TypedDict — define ALL fields BEFORE writing any node function."""

from typing import TypedDict, List, Optional


class CapstoneState(TypedDict):
    # Core input / routing
    question: str
    route: str                   # "retrieve" | "tool" | "skip"

    # Conversation memory (sliding window stored here)
    messages: List[dict]         # [{"role": "user"|"assistant", "content": "..."}]
    user_name: Optional[str]     # extracted once from "my name is X"

    # Retrieval output
    retrieved: str               # formatted context string from ChromaDB
    sources: List[str]           # list of topic labels returned by retrieval

    # Tool output
    tool_result: str             # string result from whichever tool was called

    # Answer + self-reflection
    answer: str
    faithfulness: float          # 0.0–1.0 scored by eval_node
    eval_retries: int            # incremented by eval_node; capped at MAX_EVAL_RETRIES

    # E-commerce domain-specific
    order_id: Optional[str]      # extracted from question if customer mentions an order ID
