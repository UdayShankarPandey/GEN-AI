from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_mistralai import ChatMistralAI

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mistral Chat",
    page_icon="🌬️",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0d0f14 !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stMain"] { background: #0d0f14 !important; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }

.chat-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.chat-header .badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99,179,237,0.08);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #63b3ed;
    margin-bottom: 16px;
}
.chat-header h1 {
    font-size: 2rem;
    font-weight: 600;
    color: #f0f4f8;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
.chat-header p {
    color: #64748b;
    font-size: 0.875rem;
    margin-top: 6px;
}

.chat-wrapper {
    max-width: 720px;
    margin: 0 auto;
    padding: 0 1rem 8rem;
}

.msg-row {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    animation: fadeUp 0.25s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.msg-row.user { flex-direction: row-reverse; }

.avatar {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
    margin-top: 2px;
}
.avatar.user-av  { background: linear-gradient(135deg,#3b82f6,#6366f1); }
.avatar.bot-av   { background: linear-gradient(135deg,#0ea5e9,#06b6d4); }

.bubble {
    max-width: 78%;
    padding: 12px 16px;
    border-radius: 16px;
    font-size: 0.9rem;
    line-height: 1.65;
    word-break: break-word;
}
.bubble.user {
    background: linear-gradient(135deg,#3b82f6,#4f46e5);
    color: #fff;
    border-bottom-right-radius: 4px;
}
.bubble.bot {
    background: #1a1f2e;
    border: 1px solid #252d3d;
    color: #c8d3e0;
    border-bottom-left-radius: 4px;
}

.ts {
    font-size: 10px;
    color: #3d4a5c;
    margin-top: 4px;
    font-family: 'JetBrains Mono', monospace;
}
.msg-row.user .ts { text-align: right; }

.empty-state {
    text-align: center;
    padding: 4rem 1rem;
    color: #2d3748;
}
.empty-state .icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-state p { font-size: 0.875rem; }

[data-testid="stBottom"] {
    background: linear-gradient(to top, #0d0f14 70%, transparent) !important;
    padding: 1rem 0 1.5rem !important;
}
[data-testid="stChatInput"] {
    background: #141825 !important;
    border: 1px solid #252d3d !important;
    border-radius: 14px !important;
    color: #f0f4f8 !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}
[data-testid="stChatInput"] textarea {
    color: #f0f4f8 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #3d4a5c !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #252d3d; border-radius: 4px; }

.info-bar {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-bottom: 1.5rem;
}
.info-chip {
    background: #141825;
    border: 1px solid #252d3d;
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 11px;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
}
.info-chip span { color: #63b3ed; }
</style>
""",
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "ended" not in st.session_state:
    st.session_state.ended = False

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="chat-header">
    <div class="badge">🌬️ &nbsp; Mistral Small 2603</div>
    <h1>What can I help with?</h1>
    <p>Type <code style="background:#141825;padding:2px 7px;border-radius:5px;color:#63b3ed">0</code> to end the session</p>
</div>
""",
    unsafe_allow_html=True,
)

# ── Stats bar ─────────────────────────────────────────────────────────────────
msg_count = len(st.session_state.history)
turns = msg_count // 2
st.markdown(
    f"""
<div class="info-bar">
    <div class="info-chip">messages &nbsp;<span>{msg_count}</span></div>
    <div class="info-chip">turns &nbsp;<span>{turns}</span></div>
    <div class="info-chip">model &nbsp;<span>mistral-small-2603</span></div>
</div>
""",
    unsafe_allow_html=True,
)

# ── Chat history ──────────────────────────────────────────────────────────────
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

if not st.session_state.history:
    st.markdown(
        """
    <div class="empty-state">
        <div class="icon">💬</div>
        <p>Send a message to start the conversation</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
else:
    for entry in st.session_state.history:
        if entry["role"] == "user":
            st.markdown(
                f"""
            <div class="msg-row user">
                <div>
                    <div class="bubble user">{entry["text"]}</div>
                    <div class="ts">{entry["time"]}</div>
                </div>
                <div class="avatar user-av">👤</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
            <div class="msg-row bot">
                <div class="avatar bot-av">🌬️</div>
                <div>
                    <div class="bubble bot">{entry["text"]}</div>
                    <div class="ts">{entry["time"]}</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

st.markdown("</div>", unsafe_allow_html=True)

# ── Session ended banner ───────────────────────────────────────────────────────
if st.session_state.ended:
    st.markdown(
        """
    <div style="text-align:center;padding:1.5rem;background:#141825;border:1px solid #252d3d;
                border-radius:14px;margin:1rem auto;max-width:400px;">
        <div style="font-size:1.5rem;margin-bottom:8px">👋</div>
        <div style="color:#c8d3e0;font-weight:500">Session ended</div>
        <div style="color:#475569;font-size:0.8rem;margin-top:4px">Refresh the page to start a new chat</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.stop()

# ── Input ─────────────────────────────────────────────────────────────────────
from datetime import datetime

prompt = st.chat_input("Message Mistral…")

if prompt:
    now = datetime.now().strftime("%H:%M")

    # mirrors original: if prompt == "0": break
    if prompt.strip() == "0":
        st.session_state.history.append({"role": "user", "text": prompt, "time": now})
        st.session_state.ended = True
        st.rerun()

    # append user message
    st.session_state.history.append({"role": "user", "text": prompt, "time": now})

    # mirrors original: model.invoke(prompt)
    with st.spinner(""):
        model = ChatMistralAI(model="mistral-small-2603")
        res = model.invoke(prompt)

    bot_time = datetime.now().strftime("%H:%M")
    st.session_state.history.append(
        {"role": "bot", "text": res.content, "time": bot_time}
    )

    st.rerun()
