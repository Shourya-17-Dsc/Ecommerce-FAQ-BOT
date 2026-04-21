"""
Streamlit UI module for the ShopEasy E-Commerce FAQ Bot.
Run: streamlit run ecommerce_bot/ui/app.py
"""

import uuid
import streamlit as st

st.set_page_config(
    page_title="ShopEasy Support Bot",
    page_icon="🛒",
    layout="wide",
)


@st.cache_resource
def load_agent():
    import agent  # noqa: F401
    from agent import ask
    return ask


def new_conversation():
    st.session_state.messages  = []
    st.session_state.thread_id = str(uuid.uuid4())


if "messages"  not in st.session_state: st.session_state.messages  = []
if "thread_id" not in st.session_state: st.session_state.thread_id = str(uuid.uuid4())


with st.sidebar:
    st.markdown("## 🛒 ShopEasy")
    st.markdown("*Your 24/7 online shopping assistant*")
    st.divider()
    st.markdown("**I can help with:**")
    st.markdown(
        "- Return & refund policy\n"
        "- Order tracking\n"
        "- Shipping & delivery\n"
        "- Payment methods & COD\n"
        "- Coupons & discounts\n"
        "- Product warranty\n"
        "- Exchange policy\n"
        "- Account & loyalty points\n"
        "- Seller & brand policies\n"
        "- Customer support contact"
    )
    st.divider()
    if st.button("🔄 New Conversation", use_container_width=True):
        new_conversation()
        st.rerun()
    st.caption("Powered by LangGraph · ChromaDB · Groq LLaMA-3.3-70B")


st.title("🛒 ShopEasy Customer Support")
st.caption("Ask me anything about orders, returns, shipping, or payments.")

ask_fn = load_agent()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your question…"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Looking that up…"):
            try:
                result      = ask_fn(question=prompt, thread_id=st.session_state.thread_id)
                answer      = result["answer"]
                route       = result["route"]
                faithfulness = result["faithfulness"]
                sources     = result["sources"]
            except Exception as exc:
                answer, route, faithfulness, sources = (
                    f"Sorry, technical issue: {exc}. Call 1800-123-4567.", "error", 0.0, []
                )

        st.markdown(answer)
        with st.expander("ℹ️ Details", expanded=False):
            c1, c2 = st.columns(2)
            c1.metric("Route", route.capitalize())
            c2.metric("Faithfulness", f"{faithfulness:.2f}")
            if sources:
                st.markdown("**Sources:** " + ", ".join(sources))

    st.session_state.messages.append({"role": "user",      "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": answer})
