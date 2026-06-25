from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import json, re
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# ── Model & prompt ─────────────────────────────────────────────────────────────
model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are MovieSage AI, an expert movie analyst and information extraction assistant.
    Your responsibilities:
    1. Carefully read and understand the entire movie description.
    2. Extract all important movie-related information.
    3. Generate a concise and engaging plot summary.
    4. Identify key characters, themes, and notable facts.
    5. Extract factual information only from the provided text.
    6. If information is not available, return null.
    7. Never hallucinate or invent details.
    8. Return ONLY valid JSON.
    9. Do not include markdown, explanations, comments, or additional text.
    Extract the following fields:
    - title, genre, director, writers, producers, cast, release_year, runtime
    - language, country, plot_summary, main_characters, themes
    - notable_facts, awards, box_office, rating, keywords
    """,
        ),
        (
            "human",
            "Analyze the following movie description and extract all relevant information.\n\nMovie Description:\n{movie_description}",
        ),
    ]
)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="MovieSage AI", page_icon="🎬", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Space+Grotesk:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: transparent !important;
    font-family: 'Space Grotesk', sans-serif;
    color: #dde8f0;
}
[data-testid="stAppViewContainer"] {
    background: #07000f !important;
    min-height: 100vh;
}
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Animated bg mesh ── */
.bg-mesh {
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse 60% 40% at 20% 10%, rgba(0,245,212,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 50% 50% at 80% 80%, rgba(255,0,110,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 60% 40%, rgba(157,78,221,0.05) 0%, transparent 60%);
}

/* ── Horizontal scan line sweep ── */
.scan-sweep {
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background: repeating-linear-gradient(
        180deg,
        transparent 0px, transparent 3px,
        rgba(0,245,212,0.012) 3px, rgba(0,245,212,0.012) 4px
    );
}

/* ── Main wrap ── */
.main-wrap {
    position: relative; z-index: 1;
    max-width: 900px; margin: 0 auto;
    padding: 0 1.5rem 6rem;
}

/* ══ HERO ══ */
.hero {
    padding: 3.5rem 0 3rem;
    text-align: center;
    position: relative;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.22em;
    text-transform: uppercase; color: #00f5d4;
    margin-bottom: 20px;
    opacity: 0.7;
}
.glitch-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 7vw, 5rem);
    font-weight: 800;
    color: #e0f7ff;
    letter-spacing: -0.03em;
    line-height: 0.95;
    position: relative;
    display: inline-block;
    text-shadow:
        -3px 0 0 rgba(255,0,110,0.6),
         3px 0 0 rgba(0,245,212,0.6);
}
.glitch-title .accent { color: #00f5d4; }
.hero-sub {
    font-size: 0.85rem; color: #3a4a6a;
    margin-top: 14px; letter-spacing: 0.02em;
    font-family: 'JetBrains Mono', monospace;
}

/* ══ NAV BAR ══ */
.nav-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 18px;
    background: rgba(0,245,212,0.04);
    border: 1px solid rgba(0,245,212,0.1);
    border-radius: 12px;
    margin-bottom: 2rem;
}
.nav-left {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; color: #3a4a6a;
    letter-spacing: 0.1em;
}
.nav-dot { display: inline-block; width:7px; height:7px; border-radius:50%; margin-right:8px; background:#00f5d4; animation: pulse 2s infinite; }
.nav-right {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; color: #3a4a6a;
    letter-spacing: 0.08em;
}
.nav-right span { color: #ff006e; }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

/* ══ INPUT CARD ══ */
.input-card {
    background: rgba(0,245,212,0.03);
    border: 1px solid rgba(0,245,212,0.15);
    border-radius: 20px;
    padding: 1.8rem 2rem 1.6rem;
    margin-bottom: 2rem;
    position: relative; overflow: hidden;
}
.input-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #00f5d4, #9d4edd, #ff006e, transparent);
}
.input-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px; letter-spacing: 0.18em;
    text-transform: uppercase; color: #00f5d4;
    opacity: 0.6; margin-bottom: 14px;
}

[data-testid="stTextArea"] textarea {
    background: rgba(0,0,0,0.5) !important;
    border: 1px solid rgba(0,245,212,0.2) !important;
    border-radius: 12px !important;
    color: #dde8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.9rem !important;
    min-height: 160px !important;
    resize: vertical !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(0,245,212,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,245,212,0.08) !important;
    outline: none !important;
}
[data-testid="stTextArea"] textarea::placeholder { color: #1e2d45 !important; }

/* ══ BUTTONS ══ */
div[data-testid="stVerticalBlock"] .stButton > button {
    width: 100%;
    background: linear-gradient(135deg, rgba(0,245,212,0.12), rgba(157,78,221,0.1));
    border: 1px solid rgba(0,245,212,0.3);
    border-radius: 12px;
    color: #00f5d4;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.7rem 1.2rem;
    transition: all 0.2s ease;
    letter-spacing: 0.03em;
}
div[data-testid="stVerticalBlock"] .stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,245,212,0.22), rgba(157,78,221,0.18));
    border-color: #00f5d4;
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(0,245,212,0.15);
}

/* ══ RESULT CARD ══ */
.result-card {
    background: rgba(7,0,15,0.8);
    border: 1px solid rgba(0,245,212,0.12);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,245,212,0.4), transparent);
}

/* ── Section headers ── */
.sec-head {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px; letter-spacing: 0.2em;
    text-transform: uppercase; color: #00f5d4;
    opacity: 0.55; margin-bottom: 10px;
}
.sec-value {
    font-size: 0.95rem; color: #b8cfe0; line-height: 1.65;
}

/* ── Tag pills ── */
.tags { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 4px; }
.tag {
    background: rgba(0,245,212,0.08);
    border: 1px solid rgba(0,245,212,0.18);
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 0.72rem;
    color: #00f5d4;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.04em;
}
.tag.pink {
    background: rgba(255,0,110,0.08);
    border-color: rgba(255,0,110,0.2);
    color: #ff6eaf;
}
.tag.purple {
    background: rgba(157,78,221,0.1);
    border-color: rgba(157,78,221,0.25);
    color: #c084fc;
}

/* ── Stat row ── */
.stat-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 1.5rem; }
.stat-box {
    flex: 1; min-width: 100px;
    background: rgba(0,245,212,0.04);
    border: 1px solid rgba(0,245,212,0.1);
    border-radius: 14px;
    padding: 14px 16px;
    text-align: center;
}
.stat-box .sv {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem; font-weight: 700;
    color: #00f5d4; line-height: 1;
}
.stat-box .sl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px; text-transform: uppercase;
    letter-spacing: 0.1em; color: #2a3a50;
    margin-top: 4px;
}

/* ── Raw JSON toggle ── */
.json-box {
    background: rgba(0,0,0,0.6);
    border: 1px solid rgba(0,245,212,0.1);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #4a7a6a;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 360px;
    overflow-y: auto;
    margin-top: 0.5rem;
}

/* ── Error card ── */
.error-card {
    background: rgba(255,0,110,0.06);
    border: 1px solid rgba(255,0,110,0.2);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    color: #ff6eaf;
    font-size: 0.88rem;
}

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,245,212,0.15); border-radius: 3px; }
</style>

<div class="bg-mesh"></div>
<div class="scan-sweep"></div>
""",
    unsafe_allow_html=True,
)

# ── Layout ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

# Hero
st.markdown(
    """
<div class="hero">
    <div class="hero-eyebrow">🎬 AI · Information Extraction · Groq llama-3.3-70b</div>
    <div class="glitch-title">Movie<span class="accent">Sage</span> AI</div>
    <div class="hero-sub">paste a movie description → get structured JSON intelligence</div>
</div>
""",
    unsafe_allow_html=True,
)

# Nav bar
st.markdown(
    """
<div class="nav-bar">
    <div class="nav-left"><span class="nav-dot"></span>SYSTEM ONLINE</div>
    <div class="nav-right">MODEL <span>llama-3.3-70b-versatile</span> · GROQ INFERENCE</div>
</div>
""",
    unsafe_allow_html=True,
)

# Input card
st.markdown('<div class="input-card"><div class="input-label">// Movie Description Input</div>', unsafe_allow_html=True)

movie_input = st.text_area(
    label="",
    placeholder="Paste any movie description, synopsis, Wikipedia text, or IMDb plot here…",
    height=180,
    label_visibility="collapsed",
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_btn = st.button("⚡ Analyze Movie", key="analyze")

st.markdown("</div>", unsafe_allow_html=True)

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze_btn:
    if not movie_input.strip():
        st.markdown('<div class="error-card">⚠️ Please paste a movie description before analyzing.</div>', unsafe_allow_html=True)
    else:
        with st.spinner("🎬 MovieSage is analyzing…"):
            chain = prompt | model
            response = chain.invoke({"movie_description": movie_input})
            raw = response.content.strip()

            # Strip markdown code fences if present
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            st.markdown(
                f'<div class="error-card">⚠️ Could not parse JSON response.<br><br><code>{raw[:400]}</code></div>',
                unsafe_allow_html=True,
            )
            st.stop()

        # ── Stat row ──
        st.markdown(
            f"""
<div class="stat-row">
    <div class="stat-box"><div class="sv">{data.get('release_year') or '—'}</div><div class="sl">Year</div></div>
    <div class="stat-box"><div class="sv">{data.get('runtime') or '—'}</div><div class="sl">Runtime</div></div>
    <div class="stat-box"><div class="sv">{data.get('rating') or '—'}</div><div class="sl">Rating</div></div>
    <div class="stat-box"><div class="sv">{data.get('language') or '—'}</div><div class="sl">Language</div></div>
    <div class="stat-box"><div class="sv">{data.get('country') or '—'}</div><div class="sl">Country</div></div>
</div>
""",
            unsafe_allow_html=True,
        )

        # ── Title & Genre ──
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        title = data.get("title") or "Unknown Title"
        genre = data.get("genre")
        genres = genre if isinstance(genre, list) else [genre] if genre else []

        st.markdown(
            f"""
<div class="sec-head">// Title</div>
<div class="sec-value" style="font-size:1.4rem;font-weight:700;color:#e0f7ff;font-family:'Syne',sans-serif;">{title}</div>
<div class="tags" style="margin-top:12px;">
    {"".join(f'<span class="tag purple">{g}</span>' for g in genres)}
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Plot Summary ──
        if data.get("plot_summary"):
            st.markdown(
                f"""
<div class="result-card">
    <div class="sec-head">// Plot Summary</div>
    <div class="sec-value">{data['plot_summary']}</div>
</div>
""",
                unsafe_allow_html=True,
            )

        # ── Cast & Crew ──
        cast = data.get("cast") or []
        cast_str = ", ".join(cast) if isinstance(cast, list) else cast or "—"
        director = data.get("director") or "—"
        writers = data.get("writers") or "—"
        if isinstance(writers, list):
            writers = ", ".join(writers)

        st.markdown(
            f"""
<div class="result-card">
    <div class="sec-head">// Cast & Crew</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:6px;">
        <div>
            <div style="font-size:8.5px;letter-spacing:0.12em;color:#2a3a50;font-family:'JetBrains Mono',monospace;text-transform:uppercase;margin-bottom:5px;">Director</div>
            <div class="sec-value">{director}</div>
        </div>
        <div>
            <div style="font-size:8.5px;letter-spacing:0.12em;color:#2a3a50;font-family:'JetBrains Mono',monospace;text-transform:uppercase;margin-bottom:5px;">Writers</div>
            <div class="sec-value">{writers}</div>
        </div>
    </div>
    <div style="margin-top:16px;">
        <div style="font-size:8.5px;letter-spacing:0.12em;color:#2a3a50;font-family:'JetBrains Mono',monospace;text-transform:uppercase;margin-bottom:8px;">Cast</div>
        <div class="tags">
            {"".join(f'<span class="tag">{c}</span>' for c in (cast if isinstance(cast, list) else cast_str.split(", ")))}
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # ── Themes ──
        themes = data.get("themes") or []
        if themes:
            if isinstance(themes, str):
                themes = [t.strip() for t in themes.split(",")]
            st.markdown(
                f"""
<div class="result-card">
    <div class="sec-head">// Themes</div>
    <div class="tags">
        {"".join(f'<span class="tag pink">{t}</span>' for t in themes)}
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

        # ── Awards & Box Office ──
        awards = data.get("awards") or "—"
        box_office = data.get("box_office") or "—"
        st.markdown(
            f"""
<div class="result-card">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
        <div>
            <div class="sec-head">// Awards</div>
            <div class="sec-value">{awards}</div>
        </div>
        <div>
            <div class="sec-head">// Box Office</div>
            <div class="sec-value">{box_office}</div>
        </div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # ── Keywords ──
        keywords = data.get("keywords") or []
        if keywords:
            if isinstance(keywords, str):
                keywords = [k.strip() for k in keywords.split(",")]
            st.markdown(
                f"""
<div class="result-card">
    <div class="sec-head">// Keywords</div>
    <div class="tags">
        {"".join(f'<span class="tag">{k}</span>' for k in keywords)}
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

        # ── Raw JSON toggle ──
        with st.expander("🔧 View Raw JSON"):
            st.markdown(
                f'<div class="json-box">{json.dumps(data, indent=2)}</div>',
                unsafe_allow_html=True,
            )

st.markdown("</div>", unsafe_allow_html=True)  # main-wrap
