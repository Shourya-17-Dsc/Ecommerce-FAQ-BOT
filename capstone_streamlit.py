"""
capstone_streamlit.py  —  ShopEasy AI FAQ Bot  (Agentic AI Capstone 2026)
Run: streamlit run capstone_streamlit.py
"""

# ── Fix Python path so 'ecommerce_bot' package is found ──────────────────────
import sys, os

# Force UTF-8 stdout/stderr so emoji/Unicode in print() never crash on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass  # Python < 3.7 fallback — shouldn't apply here

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Load .env BEFORE any other import that reads env vars ─────────────────────
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

import uuid
import html as html_lib   # stdlib html.escape — prevents HTML injection bugs
import streamlit as st

# ── Page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="ShopEasy AI Support",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# PREMIUM CSS  (dark theme — unchanged from original, but now rendered safely)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1040 50%, #24243e 100%);
    min-height: 100vh;
}

/* ── Hide default chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 860px !important;
}

/* ══ SIDEBAR ══════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#1a0533 0%,#12002e 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] * { color: #e2d9f3 !important; }

.sidebar-brand { text-align:center; padding:1rem 0 0.4rem; }
.sidebar-brand .logo { font-size:2.6rem; display:block; margin-bottom:0.2rem; }
.sidebar-brand h2 {
    font-family:'Poppins',sans-serif; font-size:1.4rem !important; font-weight:700;
    background:linear-gradient(90deg,#ff6b35,#f7c59f);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0 !important;
}
.sidebar-brand p { font-size:0.73rem; color:rgba(226,217,243,0.5) !important; margin:0.2rem 0 0; }

.sidebar-card {
    background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07);
    border-radius:13px; padding:0.8rem 0.9rem; margin:0.6rem 0;
}
.sidebar-card h4 {
    font-size:0.68rem !important; text-transform:uppercase; letter-spacing:1.4px;
    color:rgba(226,217,243,0.4) !important; margin:0 0 0.5rem !important; font-weight:600;
}
.topic-pill {
    display:inline-flex; align-items:center; gap:5px;
    background:rgba(255,107,53,0.1); border:1px solid rgba(255,107,53,0.2);
    border-radius:20px; padding:3px 9px; font-size:0.7rem;
    color:#f7c59f !important; margin:2px 2px 0 0; white-space:nowrap;
}

/* Quick-ask buttons inside sidebar */
[data-testid="stSidebar"] .stButton > button {
    background:rgba(255,255,255,0.05) !important;
    border:1px solid rgba(255,107,53,0.3) !important; border-radius:9px !important;
    color:#f7c59f !important; font-size:0.77rem !important; font-weight:500 !important;
    padding:0.4rem 0.65rem !important; transition:all 0.2s ease !important;
    text-align:left !important; width:100% !important; margin-bottom:3px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background:rgba(255,107,53,0.18) !important;
    border-color:rgba(255,107,53,0.6) !important; transform:translateX(3px) !important;
}

/* New conversation button */
.new-chat-btn > button {
    background:linear-gradient(135deg,#ff6b35,#f7931e) !important;
    border:none !important; border-radius:11px !important; color:#fff !important;
    font-weight:600 !important; font-size:0.82rem !important;
    padding:0.5rem 1rem !important; width:100% !important;
    transition:all 0.25s ease !important; box-shadow:0 4px 15px rgba(255,107,53,0.3) !important;
}
.new-chat-btn > button:hover {
    box-shadow:0 6px 20px rgba(255,107,53,0.5) !important; transform:translateY(-1px) !important;
}

.stat-badge {
    background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.08);
    border-radius:9px; padding:0.45rem 0.6rem; text-align:center;
}
.stat-badge .label {
    font-size:0.6rem; text-transform:uppercase; letter-spacing:1px;
    color:rgba(226,217,243,0.38) !important; display:block;
}
.stat-badge .value { font-size:0.88rem; font-weight:700; color:#ff6b35 !important; }
.sidebar-divider { border:none; border-top:1px solid rgba(255,255,255,0.07); margin:0.7rem 0; }
.tech-tag {
    display:inline-block; background:rgba(255,255,255,0.05);
    border-radius:5px; padding:2px 7px; font-size:0.63rem;
    color:rgba(226,217,243,0.45) !important; margin:2px;
}

/* ══ HERO BANNER ══════════════════════════════════════════════════════════ */
.hero-banner {
    background:linear-gradient(135deg,rgba(255,107,53,0.13) 0%,rgba(138,43,226,0.13) 100%);
    border:1px solid rgba(255,107,53,0.18); border-radius:18px;
    padding:1.5rem 1.8rem; margin-bottom:1.2rem;
    display:flex; align-items:center; gap:1.1rem; backdrop-filter:blur(10px);
}
.hero-icon { font-size:2.8rem; line-height:1; }
.hero-text h1 {
    font-family:'Poppins',sans-serif; font-size:1.8rem !important; font-weight:700;
    background:linear-gradient(90deg,#ff6b35,#f7c59f,#c084fc);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    margin:0 0 0.2rem !important; line-height:1.2;
}
.hero-text p { color:rgba(226,217,243,0.62); font-size:0.83rem; margin:0; line-height:1.5; }
.status-dot {
    display:inline-block; width:7px; height:7px; background:#22c55e;
    border-radius:50%; margin-right:4px; animation:pulse 2s infinite;
}
@keyframes pulse {
    0%,100%{ opacity:1; box-shadow:0 0 0 0 rgba(34,197,94,0.4); }
    50%     { opacity:0.8; box-shadow:0 0 0 5px rgba(34,197,94,0); }
}

/* ══ CHAT BUBBLES ══════════════════════════════════════════════════════════ */
.user-bubble { display:flex; justify-content:flex-end; margin:0.5rem 0; }
.user-bubble .bubble {
    background:linear-gradient(135deg,#ff6b35,#f7931e); color:#fff;
    border-radius:18px 18px 4px 18px; padding:0.7rem 1rem; max-width:78%;
    font-size:0.87rem; line-height:1.55;
    box-shadow:0 4px 14px rgba(255,107,53,0.28); word-wrap:break-word;
}

.bot-bubble { display:flex; justify-content:flex-start; margin:0.5rem 0; gap:0.55rem; align-items:flex-start; }
.bot-avatar {
    width:34px; height:34px;
    background:linear-gradient(135deg,#6d28d9,#a855f7); border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:0.95rem; flex-shrink:0; margin-top:2px;
    box-shadow:0 3px 10px rgba(168,85,247,0.38);
}
.bot-bubble .bubble {
    background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1);
    color:#e9e0ff; border-radius:4px 18px 18px 18px;
    padding:0.7rem 1rem; max-width:78%; font-size:0.87rem; line-height:1.6;
    backdrop-filter:blur(8px); word-wrap:break-word;
}

/* Meta badges removed — no longer rendered */

/* ── Welcome card ── */
.welcome-card {
    background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07);
    border-radius:15px; padding:1.4rem; text-align:center; margin:1.5rem auto; max-width:500px;
}
.welcome-card h3 { color:#f7c59f; font-family:'Poppins',sans-serif; margin-bottom:0.4rem; }
.welcome-card p  { color:rgba(226,217,243,0.58); font-size:0.83rem; line-height:1.5; }

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {
    background:rgba(255,255,255,0.06) !important;
    border:1.5px solid rgba(255,107,53,0.28) !important; border-radius:13px !important;
    color:#f1eaff !important; font-family:'Inter',sans-serif !important;
    font-size:0.87rem !important; padding:0.7rem 0.95rem !important;
    transition:border-color 0.2s !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color:rgba(255,107,53,0.65) !important;
    box-shadow:0 0 0 3px rgba(255,107,53,0.1) !important;
}
[data-testid="stChatInput"] textarea::placeholder { color:rgba(226,217,243,0.28) !important; }
[data-testid="stChatInputSubmitButton"] button {
    background:linear-gradient(135deg,#ff6b35,#f7931e) !important;
    border-radius:9px !important; border:none !important;
}

/* Spinner */
.stSpinner > div { border-top-color:#ff6b35 !important; }

/* Scrollbar */
::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:rgba(255,107,53,0.28); border-radius:10px; }
::-webkit-scrollbar-thumb:hover { background:rgba(255,107,53,0.55); }

/* Error box */
.err-box {
    background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3);
    border-radius:10px; padding:0.8rem 1rem; color:#fca5a5;
    font-size:0.82rem; margin-top:6px;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# AGENT INITIALISATION  (cached — runs once per Streamlit session)
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner="🚀 Loading ShopEasy AI — hang tight…")
def _init_agent():
    """
    Import agent.py and return the ask() function.
    Returns (ask_fn, None) on success or (None, error_message) on failure.
    """
    try:
        import agent                   # triggers KB build + LangGraph compile
        return agent.ask, None
    except Exception as exc:
        import traceback
        return None, traceback.format_exc()


ask_fn, init_error = _init_agent()


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def _reset_session():
    st.session_state.messages   = []          # list of {role, content, meta?}
    st.session_state.thread_id  = str(uuid.uuid4())
    st.session_state.turn_count = 0


if "messages" not in st.session_state:
    _reset_session()


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span class="logo">🛍️</span>
        <h2>ShopEasy</h2>
        <p><span class="status-dot"></span>AI Support &nbsp;·&nbsp; Online 24/7</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # Topics I can help with
    st.markdown("""
    <div class="sidebar-card">
        <h4>💡 Topics I Can Help With</h4>
        <span class="topic-pill">📦 Returns</span>
        <span class="topic-pill">💸 Refunds</span>
        <span class="topic-pill">🚚 Shipping</span>
        <span class="topic-pill">💳 Payments</span>
        <span class="topic-pill">🏷️ Coupons</span>
        <span class="topic-pill">🔄 Exchange</span>
        <span class="topic-pill">🛡️ Warranty</span>
        <span class="topic-pill">⭐ SuperCoins</span>
        <span class="topic-pill">📍 Order Track</span>
        <span class="topic-pill">📷 Damaged Item</span>
        <span class="topic-pill">🏪 Sellers</span>
        <span class="topic-pill">👤 Account</span>
    </div>
    """, unsafe_allow_html=True)

    # Quick questions
    st.markdown("""
    <div class="sidebar-card">
        <h4>⚡ Quick Questions</h4>
    </div>
    """, unsafe_allow_html=True)

    QUICK_QS = [
        ("📦", "What is the return policy?"),
        ("📍", "How do I track my order?"),
        ("💳", "Does ShopEasy have Cash on Delivery?"),
        ("🏷️", "How do I apply a coupon code?"),
        ("🔄", "How do I exchange a product?"),
        ("⭐", "How do SuperCoins work?"),
    ]
    for icon, question in QUICK_QS:
        if st.button(f"{icon}  {question}", key=f"qbtn_{question}",
                     use_container_width=True):
            # Store in session state — processed BELOW in main loop
            st.session_state["_pending_q"] = question
            st.rerun()

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # Stats row
    c1, c2 = st.columns(2)
    tid_short = f"#{st.session_state['thread_id'][:6].upper()}"
    turns     = st.session_state.get("turn_count", 0)
    c1.markdown(f"""
        <div class="stat-badge">
            <span class="label">Session</span>
            <span class="value">{tid_short}</span>
        </div>""", unsafe_allow_html=True)
    c2.markdown(f"""
        <div class="stat-badge">
            <span class="label">Turns</span>
            <span class="value">{turns}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # New conversation button
    st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
    if st.button("✨  Start New Conversation", key="new_conv_btn",
                 use_container_width=True):
        _reset_session()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # Tech stack footer
    st.markdown("""
    <div style="text-align:center; padding-bottom:0.4rem">
        <span class="tech-tag">LangGraph</span>
        <span class="tech-tag">ChromaDB</span>
        <span class="tech-tag">Groq LLaMA-3.3</span>
        <span class="tech-tag">Streamlit</span>
        <br><br>
        <span style="font-size:0.62rem;color:rgba(226,217,243,0.28)">
            Agentic AI Capstone · 2026
        </span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HERO BANNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-banner">
    <div class="hero-icon">🛍️</div>
    <div class="hero-text">
        <h1>ShopEasy Customer Support</h1>
        <p>
            <span class="status-dot"></span>
            AI-powered &nbsp;·&nbsp; Instant answers &nbsp;·&nbsp; Available 24/7<br>
            Returns &nbsp;·&nbsp; Shipping &nbsp;·&nbsp; Payments &nbsp;·&nbsp;
            Orders &nbsp;·&nbsp; Coupons &nbsp;·&nbsp; Warranty
        </p>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STARTUP ERROR GUARD
# ══════════════════════════════════════════════════════════════════════════════
if init_error:
    st.error("⚠️ Agent failed to initialise. Check your GROQ_API_KEY in the .env file.")
    with st.expander("🔍 Full error trace (for debugging)"):
        st.code(init_error, language="python")
    st.stop()   # halt rendering — don't show chat UI


# ══════════════════════════════════════════════════════════════════════════════
# RENDER HELPERS  (HTML-safe: always escape user/bot text)
# ══════════════════════════════════════════════════════════════════════════════
def _render_user(text: str):
    safe = html_lib.escape(text).replace("\n", "<br>")
    # Single compact string — no blank lines (blank lines end Markdown HTML blocks prematurely)
    st.markdown(
        f'<div class="user-bubble"><div class="bubble">{safe}</div></div>',
        unsafe_allow_html=True,
    )


def _render_bot(text: str, meta: dict | None = None):
    safe = html_lib.escape(text).replace("\n", "<br>")
    # Single compact HTML string — NO blank lines inside (blank lines break Markdown HTML blocks)
    st.markdown(
        f'<div class="bot-bubble">'
        f'<div class="bot-avatar">🤖</div>'
        f'<div class="bubble">{safe}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# WELCOME CARD (shown only when chat is empty)
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <div style="font-size:2.4rem;margin-bottom:0.4rem">👋</div>
        <h3>Hi! I'm your ShopEasy Assistant</h3>
        <p>Ask me anything about your orders, returns, payments, shipping,<br>
        coupons, or any ShopEasy policy — I'm here to help instantly.</p>
        <div style="display:flex;flex-wrap:wrap;gap:7px;justify-content:center;margin-top:0.9rem">
            <span style="background:rgba(255,107,53,0.1);border:1px solid rgba(255,107,53,0.22);
                border-radius:18px;padding:4px 12px;font-size:0.76rem;color:#f7c59f;">
                📦 Return Policy</span>
            <span style="background:rgba(255,107,53,0.1);border:1px solid rgba(255,107,53,0.22);
                border-radius:18px;padding:4px 12px;font-size:0.76rem;color:#f7c59f;">
                🚚 Shipping Info</span>
            <span style="background:rgba(255,107,53,0.1);border:1px solid rgba(255,107,53,0.22);
                border-radius:18px;padding:4px 12px;font-size:0.76rem;color:#f7c59f;">
                💳 Payment Options</span>
            <span style="background:rgba(255,107,53,0.1);border:1px solid rgba(255,107,53,0.22);
                border-radius:18px;padding:4px 12px;font-size:0.76rem;color:#f7c59f;">
                ⭐ SuperCoins</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# REPLAY CONVERSATION  (all messages from session state)
# ══════════════════════════════════════════════════════════════════════════════
for msg in st.session_state.messages:
    if msg["role"] == "user":
        _render_user(msg["content"])
    else:
        _render_bot(msg["content"], msg.get("meta"))


# ══════════════════════════════════════════════════════════════════════════════
# CHAT INPUT  — ALWAYS rendered (critical for Streamlit widget stability)
# ══════════════════════════════════════════════════════════════════════════════
chat_input = st.chat_input("Ask me anything about ShopEasy…", key="main_chat_input")

# Resolve prompt: sidebar-button press takes priority over typed input
prompt: str | None = st.session_state.pop("_pending_q", None) or chat_input


# ══════════════════════════════════════════════════════════════════════════════
# PROCESS NEW PROMPT
# ══════════════════════════════════════════════════════════════════════════════
if prompt:
    prompt = prompt.strip()
    if not prompt:
        st.stop()

    # 1. Append user message to session state immediately
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Call agent
    with st.spinner("🔍 Looking that up for you…"):
        try:
            result       = ask_fn(question=prompt, thread_id=st.session_state["thread_id"])
            answer       = result.get("answer", "").strip() or "I'm sorry, I couldn't generate a response. Please try again."
            route        = result.get("route", "retrieve")
            faithfulness = float(result.get("faithfulness", 1.0))
            sources      = result.get("sources", [])
            err_detail   = None
        except Exception as exc:
            import traceback
            answer       = ("I'm sorry, I hit a technical issue. "
                            "Please call **1800-123-4567** (Mon–Sat, 9 AM–9 PM) "
                            "or email support@shopeasy.in for assistance.")
            route        = "error"
            faithfulness = 0.0
            sources      = []
            err_detail   = traceback.format_exc()

    # 3. Append bot response to session state
    meta = {"route": route, "faithfulness": faithfulness, "sources": sources}
    st.session_state.messages.append({
        "role":    "assistant",
        "content": answer,
        "meta":    meta,
    })
    st.session_state["turn_count"] = st.session_state.get("turn_count", 0) + 1

    # 4. Show technical error details in an expander (non-blocking)
    if err_detail:
        with st.expander("⚠️ Technical details"):
            st.code(err_detail, language="python")

    # 5. Rerun so the replay loop above shows all messages cleanly
    st.rerun()
