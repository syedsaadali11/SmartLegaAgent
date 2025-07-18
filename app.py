# app.py

import os
import sys
import uuid
import streamlit as st
from dotenv import load_dotenv

# ------------------------------------------------------------------
# Import project modules (ensure package path)
# ------------------------------------------------------------------
ROOT_DIR = os.path.dirname(__file__)
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from graph.graph import run_graph
from utils.state import AgentState
from utils.logger import log_interaction

# ------------------------------------------------------------------
# Env
# ------------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------------
# Streamlit Config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="SmartLegalAgent",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"  # ensure sidebar is open in chat
)

# ------------------------------------------------------------------
# Session State Init
# ------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "show_disclaimer" not in st.session_state:
    st.session_state.show_disclaimer = True

# ==================================================================
# ---------------------- GLOBAL STYLES ------------------------------
# ==================================================================
st.markdown(
    """
<style>
footer {visibility: hidden;}
/* Landing page colours */
.landing-wrapper {
    height: 90vh;
    display: flex;
    flex-direction: column;
    align-items:center;
    justify-content:center;
    text-align:center;
    padding: 0 1rem;
}
.landing-title {
    font-size: clamp(2.7rem, 5vw, 4.2rem);
    font-weight: 800;
    color: #FFFF00;
    margin-bottom: 0.25em;
}
.landing-sub {
    font-size: clamp(1.3rem, 2vw, 1.8rem);
    color: #FFFF00;
    font-weight: 600;
    margin-bottom: 1.2em;
}
.landing-desc {
    font-size: 1.15rem;
    max-width: 800px;
    color: #FFFFFF;
    line-height: 1.7;
    margin: 0 auto 2em;
}
[data-testid="stAppViewContainer"] {
    background-color: #111111;
    color: #FFFFFF;
}
.sla-landing-btn > button {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    font-size: 1.2rem !important;
    border-radius: 10px !important;
    border: 2px solid #FFFF00 !important;
}
.sla-landing-btn > button:hover {
    background-color: #222222 !important;
}
[data-testid="stSidebar"] {
    background-color: #1b1b1b;
}
</style>
""",
    unsafe_allow_html=True,
)

# ==================================================================
# -------------------------- LANDING PAGE --------------------------
# ==================================================================
def render_landing():
    # Hide sidebar explicitly while on landing
    st.markdown(
        "<style>[data-testid='stSidebar']{display:none;}</style>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="landing-wrapper">
            <div class="landing-title">⚖️ SmartLegalAgent</div>
            <div class="landing-sub">Your AI‑Powered Legal Companion for Pakistani Law</div>
            <div class="landing-desc">
                Ask any question about Pakistani statutes, offences, cyber laws, constitutional rights, or criminal procedure.
                Get fast, reference‑anchored answers — powered by AI + authoritative legal sources.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<div class='sla-landing-btn'>", unsafe_allow_html=True)
        if st.button("🚪 Your Legal Journey Starts Here", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ==================================================================
# -------------------------- SIDEBAR (CHAT) ------------------------
# ==================================================================
def render_chat_sidebar():
    with st.sidebar:
        st.header("SmartLegalAgent")

        if st.button("🏠 Home"):
            st.session_state.page = "landing"
            st.rerun()

        if st.button("🆕 New Chat"):
            st.session_state.chat_history = []
            st.session_state.page = "chat"
            st.rerun()

        st.markdown("---")
        st.subheader("ℹ️ More")

        if st.button("📄 About"):
            st.session_state.page = "about"
            st.rerun()

        if st.button("📬 Contact"):
            st.session_state.page = "contact"
            st.rerun()


# ==================================================================
# ------------------ CHAT MESSAGE RENDER ---------------------------
# ==================================================================
def render_chat_history():
    for entry in st.session_state.chat_history:
        if len(entry) == 3:
            role, _, text = entry
        else:
            role, text = entry
        with st.chat_message(role):
            st.markdown(text)

# ==================================================================
# --------------------------- CHAT PAGE ----------------------------
# ==================================================================
def render_chat_page():
    render_chat_sidebar()

    st.title("⚖️ SmartLegalAgent")
    st.write("Ask a legal question. Your friendly AI assistant is here to help!")

    render_chat_history()

    user_q = st.chat_input("Enter your legal question…")
    if user_q:
        msg_id = uuid.uuid4().hex
        st.session_state.chat_history.append(("user", msg_id, user_q))

        init_state = AgentState(question=user_q)
        final_state = run_graph(init_state)

        answer = (final_state.answer or "Sorry, I couldn't generate an answer.").strip()
        asst_id = uuid.uuid4().hex
        st.session_state.chat_history.append(("assistant", asst_id, answer))

        log_interaction(user_q, answer)
        st.rerun()


# ==================================================================
# ------------------------ ABOUT PAGE ------------------------------
# ==================================================================
def render_about_page():
    render_chat_sidebar()
    st.title("📄 About SmartLegalAgent")
    st.markdown("""
    SmartLegalAgent is your personal legal assistant powered by AI.
    
    It provides Pakistani citizens with quick, easy-to-understand answers regarding:
    - Laws and statutes
    - Offences and punishments
    - Cyber laws and constitutional rights

    ⚖️ Empowering you with legal knowledge, not legal representation.
    """)

# ==================================================================
# ------------------------ CONTACT PAGE ----------------------------
# ==================================================================
def render_contact_page():
    render_chat_sidebar()
    st.title("📬 Contact Us")
    st.markdown("""
    For feedback, support, or queries, please reach out:
    
    📧 **Email**: support@smartlegalagent.pk  
    🌐 **Website**: [www.smartlegalagent.pk](http://www.smartlegalagent.pk)  
    📱 **WhatsApp**: +92-xxx-xxxxxxx
    """)

# ==================================================================
# ------------------------------ ROUTER -----------------------------
# ==================================================================
if st.session_state.page == "landing":
    render_landing()
elif st.session_state.page == "about":
    render_about_page()
elif st.session_state.page == "contact":
    render_contact_page()
else:
    render_chat_page()
