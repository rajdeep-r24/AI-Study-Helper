import streamlit as st
import google.generativeai as genai
import json
import time
import random
import io
import re
from datetime import datetime

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ExamForge AI — Final Prep Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)



# ─── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,400;0,500;1,400&family=Outfit:wght@300;400;500;600;700&display=swap');

:root {
  --bg: #04050a;
  --bg2: #090b14;
  --surface: #0d1120;
  --surface2: #121829;
  --border: rgba(99,102,241,0.18);
  --accent: #6366f1;
  --accent2: #22d3ee;
  --accent3: #f59e0b;
  --accent4: #10b981;
  --danger: #ef4444;
  --text: #e2e8f0;
  --muted: #64748b;
  --glow: rgba(99,102,241,0.35);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Outfit', sans-serif;
  font-size: 15px;
}

/* Animated starfield background */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 50% -20%, rgba(99,102,241,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 85% 80%, rgba(34,211,238,0.07) 0%, transparent 55%),
    radial-gradient(ellipse 60% 50% at 10% 90%, rgba(245,158,11,0.06) 0%, transparent 55%);
  pointer-events: none;
  z-index: 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 1rem !important; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px; }

/* ── PERMANENTLY LOCK SIDEBAR OPEN — hide collapse/expand button ── */
button[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[kind="header"],
section[data-testid="stSidebar"] button[data-testid="baseButton-header"],
.st-emotion-cache-czk5ss,
.st-emotion-cache-1wbqy5l,
div[data-testid="collapsedControl"] {
  display: none !important;
  visibility: hidden !important;
  pointer-events: none !important;
}
/* Keep sidebar always at full width — never let it collapse */
section[data-testid="stSidebar"] {
  min-width: 280px !important;
  max-width: 320px !important;
  transform: none !important;
  left: 0 !important;
  visibility: visible !important;
  display: block !important;
}

/* ── HERO ── */
.hero {
  text-align: center;
  padding: 3.5rem 1rem 2.5rem;
  position: relative;
}
.hero-badge {
  display: inline-block;
  background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(34,211,238,0.15));
  border: 1px solid rgba(99,102,241,0.4);
  border-radius: 100px;
  padding: 6px 20px;
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  letter-spacing: 2px;
  color: var(--accent2);
  margin-bottom: 1.4rem;
  text-transform: uppercase;
  animation: pulse-badge 3s ease-in-out infinite;
}
@keyframes pulse-badge {
  0%,100% { box-shadow: 0 0 0 0 rgba(34,211,238,0); }
  50% { box-shadow: 0 0 20px 4px rgba(34,211,238,0.2); }
}
.hero h1 {
  font-family: 'Syne', sans-serif;
  font-weight: 800;
  font-size: clamp(2.4rem, 5vw, 4.2rem);
  line-height: 1.08;
  background: linear-gradient(135deg, #e2e8f0 0%, #6366f1 45%, #22d3ee 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
  animation: shimmer 4s linear infinite;
  background-size: 200% 100%;
}
@keyframes shimmer {
  0% { background-position: 200% center; }
  100% { background-position: -200% center; }
}
.hero p {
  color: var(--muted);
  font-size: 1.05rem;
  max-width: 600px;
  margin: 0 auto 2rem;
  line-height: 1.7;
}

/* ── STATS BAR ── */
.stats-bar {
  display: flex;
  justify-content: center;
  gap: 2.5rem;
  flex-wrap: wrap;
  margin-bottom: 2.5rem;
}
.stat-pill {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 14px 28px;
  text-align: center;
  position: relative;
  overflow: hidden;
  animation: float 4s ease-in-out infinite;
  cursor: default;
  transition: transform 0.3s, box-shadow 0.3s;
}
.stat-pill:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(99,102,241,0.25);
}
.stat-pill::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: conic-gradient(transparent, rgba(99,102,241,0.08), transparent 30%);
  animation: spin 6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes float {
  0%,100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}
.stat-number {
  font-family: 'Syne', sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--accent2);
}
.stat-label {
  font-size: 0.72rem;
  color: var(--muted);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-top: 2px;
}

/* ── NAV TABS ── */
.nav-tabs {
  display: flex;
  gap: 8px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 6px;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}
.nav-tab {
  flex: 1;
  min-width: 120px;
  background: transparent;
  border: none;
  border-radius: 12px;
  padding: 12px 16px;
  color: var(--muted);
  font-family: 'Outfit', sans-serif;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  white-space: nowrap;
}
.nav-tab.active {
  background: linear-gradient(135deg, var(--accent), #4f46e5);
  color: white;
  box-shadow: 0 4px 20px rgba(99,102,241,0.4);
  transform: translateY(-1px);
}
.nav-tab:hover:not(.active) {
  background: rgba(99,102,241,0.1);
  color: var(--text);
}

/* ── CARDS ── */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 1.6rem;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s, box-shadow 0.3s;
}
.card:hover {
  border-color: rgba(99,102,241,0.35);
  box-shadow: 0 8px 40px rgba(99,102,241,0.12);
}
.card::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent3));
  opacity: 0;
  transition: opacity 0.3s;
}
.card:hover::after { opacity: 1; }

.card-title {
  font-family: 'Syne', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: var(--text);
  margin-bottom: 0.4rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ── FEATURE GRID ── */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin: 1.5rem 0;
}
.feature-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 1.4rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  text-align: center;
  position: relative;
  overflow: hidden;
}
.feature-card:hover {
  transform: translateY(-6px) scale(1.02);
  border-color: var(--accent);
  box-shadow: 0 20px 50px rgba(99,102,241,0.2);
}
.feature-icon {
  font-size: 2.2rem;
  margin-bottom: 0.8rem;
  display: block;
  animation: bounce-icon 2s ease-in-out infinite;
}
@keyframes bounce-icon {
  0%,100% { transform: scale(1); }
  50% { transform: scale(1.1) rotate(5deg); }
}
.feature-title {
  font-family: 'Syne', sans-serif;
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--text);
  margin-bottom: 4px;
}
.feature-desc {
  font-size: 0.75rem;
  color: var(--muted);
  line-height: 1.5;
}

/* ── BUTTONS ── */
.stButton > button {
  background: linear-gradient(135deg, var(--accent) 0%, #4f46e5 100%) !important;
  color: white !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 12px 28px !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  letter-spacing: 0.3px !important;
  cursor: pointer !important;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
  box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
  position: relative !important;
  overflow: hidden !important;
}
.stButton > button:hover {
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow: 0 8px 30px rgba(99,102,241,0.5) !important;
}
.stButton > button:active {
  transform: translateY(0) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div,
.stMultiSelect > div > div > div {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
  font-family: 'Outfit', sans-serif !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

/* Sliders */
.stSlider > div > div > div > div {
  background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
}

/* Labels */
.stTextInput label, .stTextArea label, .stSelectbox label,
.stSlider label, .stMultiSelect label, .stRadio label,
.stCheckbox label, .stNumberInput label {
  color: var(--muted) !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 0.75rem !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
}

/* Progress */
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
  border-radius: 100px !important;
}

/* ── QUESTION CARD ── */
.q-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.4rem 1.6rem;
  margin-bottom: 1rem;
  position: relative;
  overflow: hidden;
  animation: slide-up 0.4s ease forwards;
  opacity: 0;
  transform: translateY(20px);
}
.q-card:nth-child(2) { animation-delay: 0.05s; }
.q-card:nth-child(3) { animation-delay: 0.10s; }
.q-card:nth-child(4) { animation-delay: 0.15s; }
.q-card:nth-child(5) { animation-delay: 0.20s; }
.q-card:nth-child(6) { animation-delay: 0.25s; }
@keyframes slide-up {
  to { opacity: 1; transform: translateY(0); }
}
.q-card::before {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 4px;
  border-radius: 4px 0 0 4px;
}
.q-card.easy::before { background: var(--accent4); }
.q-card.medium::before { background: var(--accent3); }
.q-card.hard::before { background: var(--danger); }

.q-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 0.8rem;
}
.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 100px;
  font-size: 0.68rem;
  font-family: 'DM Mono', monospace;
  font-weight: 500;
  letter-spacing: 0.5px;
}
.badge-easy { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }
.badge-medium { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
.badge-hard { background: rgba(239,68,68,0.15); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }
.badge-bloom { background: rgba(99,102,241,0.15); color: #818cf8; border: 1px solid rgba(99,102,241,0.3); }
.badge-marks { background: rgba(34,211,238,0.12); color: #22d3ee; border: 1px solid rgba(34,211,238,0.25); }
.badge-type { background: rgba(168,85,247,0.12); color: #c084fc; border: 1px solid rgba(168,85,247,0.25); }

.q-text {
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--text);
  margin-bottom: 0.8rem;
}
.q-answer {
  background: rgba(16,185,129,0.06);
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: 10px;
  padding: 10px 14px;
  font-size: 0.85rem;
  color: #6ee7b7;
  margin-top: 8px;
}
.q-explanation {
  background: rgba(99,102,241,0.07);
  border: 1px solid rgba(99,102,241,0.2);
  border-radius: 10px;
  padding: 10px 14px;
  font-size: 0.83rem;
  color: #a5b4fc;
  margin-top: 6px;
}

/* ── FLASHCARD ── */
.flashcard-container {
  perspective: 1200px;
  height: 220px;
  cursor: pointer;
  margin-bottom: 1rem;
}
.flashcard {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.6s cubic-bezier(0.4,0,0.2,1);
  border-radius: 20px;
}
.flashcard.flipped { transform: rotateY(180deg); }
.card-face {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
  flex-direction: column;
  gap: 0.5rem;
}
.card-front {
  background: linear-gradient(135deg, var(--surface), var(--surface2));
  border: 1px solid var(--border);
}
.card-back {
  background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(34,211,238,0.1));
  border: 1px solid rgba(99,102,241,0.3);
  transform: rotateY(180deg);
}

/* ── TIMER ── */
.timer-ring {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}
.timer-display {
  font-family: 'Syne', sans-serif;
  font-size: 3.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--accent2), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-align: center;
}
.timer-warning { color: var(--accent3) !important; }
.timer-danger { color: var(--danger) !important; }

/* ── TOPIC CHIP ── */
.topic-chip {
  display: inline-block;
  background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(34,211,238,0.1));
  border: 1px solid rgba(99,102,241,0.3);
  border-radius: 100px;
  padding: 6px 16px;
  font-size: 0.8rem;
  color: #a5b4fc;
  margin: 4px;
  transition: all 0.25s;
  cursor: default;
  font-family: 'DM Mono', monospace;
}
.topic-chip:hover {
  background: rgba(99,102,241,0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(99,102,241,0.25);
}
.topic-chip.hot {
  background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(245,158,11,0.12));
  border-color: rgba(245,158,11,0.35);
  color: #fcd34d;
}

/* ── ANALYSIS CHARTS ── */
.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
  margin: 1.5rem 0;
}
.analysis-card {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.2rem;
  text-align: center;
}
.analysis-value {
  font-family: 'Syne', sans-serif;
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 4px;
}
.analysis-label {
  font-size: 0.72rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 1px;
  font-family: 'DM Mono', monospace;
}

/* ── SIDEBAR STYLES ── */
.sidebar-logo {
  font-family: 'Syne', sans-serif;
  font-weight: 800;
  font-size: 1.3rem;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  padding: 0.5rem 0 1rem;
  text-align: center;
}
.sidebar-section {
  font-family: 'DM Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
  padding: 0.8rem 0 0.4rem;
  border-top: 1px solid var(--border);
  margin-top: 0.8rem;
}

/* ── DIVIDER ── */
.gradient-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  margin: 1.5rem 0;
  opacity: 0.4;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* Expander */
.streamlit-expanderHeader {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  font-family: 'Outfit', sans-serif !important;
  color: var(--text) !important;
}

/* Success/error */
.stSuccess { background: rgba(16,185,129,0.08) !important; border-color: rgba(16,185,129,0.3) !important; }
.stError { background: rgba(239,68,68,0.08) !important; border-color: rgba(239,68,68,0.3) !important; }
.stWarning { background: rgba(245,158,11,0.08) !important; border-color: rgba(245,158,11,0.3) !important; }
.stInfo { background: rgba(99,102,241,0.08) !important; border-color: rgba(99,102,241,0.3) !important; }

/* Upload zone */
[data-testid="stFileUploader"] {
  background: var(--surface) !important;
  border: 2px dashed var(--border) !important;
  border-radius: 16px !important;
  transition: border-color 0.3s !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--accent) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-radius: 14px !important;
  padding: 4px !important;
  gap: 4px !important;
  border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px !important;
  color: var(--muted) !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--accent), #4f46e5) !important;
  color: white !important;
}

/* Metric */
[data-testid="stMetric"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
  padding: 1rem !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Syne', sans-serif !important;
  color: var(--accent2) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ───────────────────────────────────────────────────────────────
defaults = {
    "api_key": "",
    "active_tab": "home",
    "generated_paper": None,
    "question_bank": [],
    "flashcards": [],
    "imp_topics": [],
    "notes_text": "",
    "timer_seconds": 0,
    "timer_running": False,
    "timer_start": None,
    "quiz_index": 0,
    "quiz_score": 0,
    "quiz_mode": False,
    "quiz_answered": False,
    "quiz_questions": [],
    "university": "",
    "subject": "",
    "topic": "",
    "course": "",
    "branch": "",
    "year": "",
    "semester": "",
    "exam_board": "",
    "generation_count": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── HELPERS ────────────────────────────────────────────────────────────────────
def student_context() -> str:
    """Build a rich student profile string to inject into every AI prompt."""
    s = st.session_state
    parts = []
    if s.university:   parts.append(f"University: {s.university}")
    if s.course:       parts.append(f"Course: {s.course}")
    if s.branch:       parts.append(f"Branch/Stream: {s.branch}")
    if s.year:         parts.append(f"Year: {s.year}")
    if s.semester:     parts.append(f"Semester: {s.semester}")
    if s.subject:      parts.append(f"Subject: {s.subject}")
    if s.topic:        parts.append(f"Topic/Chapter: {s.topic}")
    if s.exam_board:   parts.append(f"Exam board/pattern: {s.exam_board}")
    if not parts:
        return ""
    return "Student profile:\n" + "\n".join(f"  - {p}" for p in parts) + "\n"

def get_model():
    if not st.session_state.api_key:
        return None
    try:
        genai.configure(api_key=st.session_state.api_key)
        return genai.GenerativeModel("gemini-2.5-flash")
    except Exception:
        return None

def call_gemini(prompt: str, max_tokens: int = 4096) -> str:
    model = get_model()
    if not model:
        return ""
    try:
        resp = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=max_tokens)
        )
        return resp.text
    except Exception as e:
        st.error(f"Gemini error: {e}")
        return ""

def extract_text_from_file(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    try:
        if name.endswith(".txt"):
            return uploaded_file.read().decode("utf-8", errors="ignore")
        elif name.endswith(".pdf"):
            try:
                import PyPDF2
                reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
                return "\n".join(p.extract_text() or "" for p in reader.pages)
            except ImportError:
                return uploaded_file.read().decode("utf-8", errors="ignore")
        elif name.endswith((".docx", ".doc")):
            try:
                from docx import Document
                doc = Document(io.BytesIO(uploaded_file.read()))
                return "\n".join(p.text for p in doc.paragraphs)
            except ImportError:
                return uploaded_file.read().decode("utf-8", errors="ignore")
        else:
            return uploaded_file.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""

def parse_questions_from_text(text: str) -> list:
    questions = []
    blocks = re.split(r'\n(?=Q\d+\.|Question \d+[\.:)])', text.strip())
    for i, block in enumerate(blocks):
        if not block.strip():
            continue
        lines = block.strip().splitlines()
        q_text = lines[0] if lines else block[:200]
        q_text = re.sub(r'^(Q\d+\.|Question \d+[\.:)]\s*)', '', q_text).strip()

        answer = ""
        explanation = ""
        bloom = "Knowledge"
        difficulty = "medium"
        marks = 2
        q_type = "short"

        for line in lines[1:]:
            l = line.strip()
            if l.lower().startswith("answer:") or l.lower().startswith("ans:"):
                answer = l.split(":", 1)[-1].strip()
            elif l.lower().startswith("explanation:") or l.lower().startswith("explain:"):
                explanation = l.split(":", 1)[-1].strip()
            elif l.lower().startswith("bloom"):
                bloom = l.split(":", 1)[-1].strip()
            elif l.lower().startswith("difficulty"):
                diff_val = l.split(":", 1)[-1].strip().lower()
                difficulty = diff_val if diff_val in ["easy", "medium", "hard"] else "medium"
            elif l.lower().startswith("marks"):
                try:
                    marks = int(re.search(r'\d+', l).group())
                except Exception:
                    marks = 2
            elif l.lower().startswith("type"):
                q_type = l.split(":", 1)[-1].strip().lower()

        if q_text:
            questions.append({
                "id": i + 1,
                "question": q_text,
                "answer": answer,
                "explanation": explanation,
                "bloom": bloom,
                "difficulty": difficulty,
                "marks": marks,
                "type": q_type,
            })
    return questions

def render_question_card(q: dict, show_answer: bool = True, idx: int = 0):
    diff_class = q.get("difficulty", "medium").lower()
    diff_class = diff_class if diff_class in ["easy", "medium", "hard"] else "medium"
    badge_class = f"badge-{diff_class}"
    st.markdown(f"""
    <div class="q-card {diff_class}" style="animation-delay:{idx*0.05}s">
      <div class="q-meta">
        <span class="badge {badge_class}">⚡ {q.get('difficulty','Medium').upper()}</span>
        <span class="badge badge-bloom">🧠 {q.get('bloom','Knowledge')}</span>
        <span class="badge badge-marks">📊 {q.get('marks',2)} Marks</span>
        <span class="badge badge-type">📝 {q.get('type','Short').title()}</span>
      </div>
      <div class="q-text"><strong>Q{q.get('id', idx+1)}.</strong> {q.get('question','')}</div>
      {'<div class="q-answer">✅ <strong>Answer:</strong> ' + q.get('answer','') + '</div>' if show_answer and q.get('answer') else ''}
      {'<div class="q-explanation">💡 <strong>Explanation:</strong> ' + q.get('explanation','') + '</div>' if show_answer and q.get('explanation') else ''}
    </div>
    """, unsafe_allow_html=True)

# ─── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">⚡ ExamForge AI</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">🔑 API Key</div>', unsafe_allow_html=True)
    api_key_input = st.text_input("Gemini API Key", value=st.session_state.api_key,
        type="password", placeholder="AIza...")
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.success("✓ Key saved")
    else:
        st.caption("Get free key → [aistudio.google.com](https://aistudio.google.com/app/apikey)")
    st.markdown('<div class="sidebar-section">🎓 Your Profile</div>', unsafe_allow_html=True)
    st.session_state.university = st.text_input("University / Institute",
        value=st.session_state.university, placeholder="e.g. Mumbai University")

    st.session_state.course = st.selectbox("Course / Degree",
        ["", "B.E. / B.Tech", "B.Sc", "B.Com", "B.A", "BBA", "BCA",
         "M.E. / M.Tech", "M.Sc", "MBA", "MCA", "Diploma", "Other"],
        index=(["", "B.E. / B.Tech", "B.Sc", "B.Com", "B.A", "BBA", "BCA",
                "M.E. / M.Tech", "M.Sc", "MBA", "MCA", "Diploma", "Other"]
               .index(st.session_state.course)
               if st.session_state.course in ["", "B.E. / B.Tech", "B.Sc",
               "B.Com", "B.A", "BBA", "BCA", "M.E. / M.Tech", "M.Sc",
               "MBA", "MCA", "Diploma", "Other"] else 0))

    st.session_state.branch = st.text_input("Branch / Stream",
        value=st.session_state.branch,
        placeholder="e.g. Computer Engg / Pharmacy / Commerce")

    col_y, col_s = st.columns(2)
    with col_y:
        st.session_state.year = st.selectbox("Year",
            ["", "1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"],
            index=(["", "1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"]
                   .index(st.session_state.year)
                   if st.session_state.year in ["", "1st Year", "2nd Year",
                   "3rd Year", "4th Year", "5th Year"] else 0))
    with col_s:
        st.session_state.semester = st.selectbox("Semester",
            ["", "Sem 1", "Sem 2", "Sem 3", "Sem 4",
             "Sem 5", "Sem 6", "Sem 7", "Sem 8"],
            index=(["", "Sem 1", "Sem 2", "Sem 3", "Sem 4",
                    "Sem 5", "Sem 6", "Sem 7", "Sem 8"]
                   .index(st.session_state.semester)
                   if st.session_state.semester in ["", "Sem 1", "Sem 2",
                   "Sem 3", "Sem 4", "Sem 5", "Sem 6", "Sem 7", "Sem 8"] else 0))

    st.session_state.subject = st.text_input("Subject",
        value=st.session_state.subject, placeholder="e.g. Applied Mathematics")
    st.session_state.topic = st.text_input("Chapter / Topic",
        value=st.session_state.topic, placeholder="e.g. Differential Equations")
    st.session_state.exam_board = st.text_input("Exam Board / Pattern (optional)",
        value=st.session_state.exam_board,
        placeholder="e.g. GTU / SPPU / Anna Univ")

    profile_parts = [p for p in [st.session_state.course, st.session_state.branch,
        st.session_state.year, st.session_state.semester] if p]
    if profile_parts:
        st.markdown(
            '<div style="background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.25);'
            'border-radius:10px;padding:8px 12px;margin-top:6px;font-family:monospace;'
            'font-size:0.68rem;color:#a5b4fc;line-height:1.6;">'
            + "👤 " + " · ".join(profile_parts) + "</div>",
            unsafe_allow_html=True
        )

    st.markdown('<div class="sidebar-section">📊 Session Stats</div>', unsafe_allow_html=True)
    st.metric("Papers Generated", st.session_state.generation_count)
    st.metric("Questions in Bank", len(st.session_state.question_bank))
    st.metric("Flashcards", len(st.session_state.flashcards))

    st.markdown('<div class="sidebar-section">🔗 Navigation</div>', unsafe_allow_html=True)
    tabs = {
        "home": "🏠 Home",
        "upload": "📁 Upload Notes",
        "exam_gen": "📄 Exam Generator",
        "question_bank": "🗂️ Question Bank",
        "flashcards": "🃏 Flashcards",
        "timer": "⏱️ Timed Practice",
        "pyq": "📚 PYQ Analyser",
        "imp_topics": "🔥 Imp Topics",
        "analytics": "📈 Analytics",
    }
    for key, label in tabs.items():
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.active_tab = key
            st.rerun()

# ─── MAIN CONTENT ───────────────────────────────────────────────────────────────
tab = st.session_state.active_tab

# ── HOME ────────────────────────────────────────────────────────────────────────
if tab == "home":
    st.markdown("""
    <div class="hero">
      <div class="hero-badge">✦ AI-Powered Final Prep Platform</div>
      <h1>Crack Your Exams with<br/>ExamForge AI</h1>
      <p>Upload your notes. Let AI extract the most important topics, generate exam-ready questions, build your personal question bank, and prep you with timed quizzes — all in one place.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stats-bar">
      <div class="stat-pill">
        <div class="stat-number">10K+</div>
        <div class="stat-label">Questions Generated</div>
      </div>
      <div class="stat-pill">
        <div class="stat-number">6</div>
        <div class="stat-label">Bloom's Levels</div>
      </div>
      <div class="stat-pill">
        <div class="stat-number">∞</div>
        <div class="stat-label">Exam Papers</div>
      </div>
      <div class="stat-pill">
        <div class="stat-number">100%</div>
        <div class="stat-label">AI-Powered</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-grid">
      <div class="feature-card">
        <span class="feature-icon">📁</span>
        <div class="feature-title">Upload Your Notes</div>
        <div class="feature-desc">PDF, DOCX, TXT — AI reads your notes and generates questions from YOUR syllabus</div>
      </div>
      <div class="feature-card">
        <span class="feature-icon">📄</span>
        <div class="feature-title">Exam Generator</div>
        <div class="feature-desc">Full structured exam papers with marks, difficulty, Bloom's tags & answer keys</div>
      </div>
      <div class="feature-card">
        <span class="feature-icon">🗂️</span>
        <div class="feature-title">Question Bank</div>
        <div class="feature-desc">Expected questions + sample papers in separate sections, always growing</div>
      </div>
      <div class="feature-card">
        <span class="feature-icon">🃏</span>
        <div class="feature-title">Smart Flashcards</div>
        <div class="feature-desc">Flip-card style revision for key concepts, formulas and definitions</div>
      </div>
      <div class="feature-card">
        <span class="feature-icon">⏱️</span>
        <div class="feature-title">Timed Practice</div>
        <div class="feature-desc">Simulate real exam pressure with countdown timer and instant scoring</div>
      </div>
      <div class="feature-card">
        <span class="feature-icon">📚</span>
        <div class="feature-title">PYQ Analyser</div>
        <div class="feature-desc">Extract patterns from past year questions of your specific university</div>
      </div>
      <div class="feature-card">
        <span class="feature-icon">🔥</span>
        <div class="feature-title">Imp Topics</div>
        <div class="feature-desc">AI identifies the hottest topics most likely to appear in your exam</div>
      </div>
      <div class="feature-card">
        <span class="feature-icon">📈</span>
        <div class="feature-title">Analytics</div>
        <div class="feature-desc">Track question difficulty distribution, topic coverage and Bloom's balance</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; padding:1rem 0 0.5rem;">
      <div style="font-family:'DM Mono',monospace; font-size:0.75rem; color:#64748b; letter-spacing:2px; text-transform:uppercase; margin-bottom:0.5rem;">How it works</div>
      <div style="display:flex; justify-content:center; gap:2rem; flex-wrap:wrap;">
        <div style="text-align:center; max-width:150px;">
          <div style="font-size:1.8rem;">①</div>
          <div style="font-size:0.8rem; color:#94a3b8; margin-top:4px;">Enter your university & subject in the sidebar</div>
        </div>
        <div style="text-align:center; max-width:150px;">
          <div style="font-size:1.8rem;">②</div>
          <div style="font-size:0.8rem; color:#94a3b8; margin-top:4px;">Upload your notes PDF/DOCX</div>
        </div>
        <div style="text-align:center; max-width:150px;">
          <div style="font-size:1.8rem;">③</div>
          <div style="font-size:0.8rem; color:#94a3b8; margin-top:4px;">Generate questions, flashcards & mock papers</div>
        </div>
        <div style="text-align:center; max-width:150px;">
          <div style="font-size:1.8rem;">④</div>
          <div style="font-size:0.8rem; color:#94a3b8; margin-top:4px;">Practice with timer, score yourself & download</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── UPLOAD NOTES ────────────────────────────────────────────────────────────────
elif tab == "upload":
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.8rem;margin-bottom:0.3rem;">
        📁 Upload Your Notes
      </div>
      <div style="color:#64748b;font-size:0.9rem;">Supports PDF, DOCX, TXT — AI will read and learn your exact syllabus</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop your notes here",
        type=["pdf", "txt", "docx", "doc"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded:
        combined = ""
        for f in uploaded:
            txt = extract_text_from_file(f)
            combined += f"\n\n--- {f.name} ---\n{txt}"
        st.session_state.notes_text = combined

        st.success(f"✅ Loaded {len(uploaded)} file(s) — {len(combined)} characters extracted")

        with st.expander("📖 Preview extracted text"):
            st.text_area("", value=combined[:3000] + ("..." if len(combined) > 3000 else ""),
                         height=300, disabled=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔥 Extract Imp Topics", use_container_width=True):
                with st.spinner("AI is analysing your notes..."):
                    prompt = f"""
You are an expert exam coach. Use the student profile below to give highly specific, targeted advice.
{student_context()}
From these notes, identify the TOP 15 most important topics MOST LIKELY to appear in their exam.
Tailor topics specifically for their course, branch and semester level — for example Maths for B.E. Computer Sem 1 is different from B.Pharm Sem 1.
For each topic give:
- Topic name
- Why it's important for their specific course/sem (1 line)
- Estimated weightage (High/Medium/Low)
- 2-3 likely question types for their exam pattern

Notes:
{combined[:8000]}

Format each topic clearly numbered.
"""
                    result = call_gemini(prompt)
                    if result:
                        st.session_state.imp_topics = result
                        st.success("Important topics extracted! Go to 🔥 Imp Topics tab.")

        with col2:
            if st.button("🃏 Generate Flashcards", use_container_width=True):
                with st.spinner("Creating flashcards..."):
                    prompt = f"""
{student_context()}
From these notes, create 15 flashcards tailored for this student's course and semester level.
Format strictly as JSON array:
[
  {{"front": "Term or question", "back": "Definition or answer", "category": "topic name"}},
  ...
]
Only return the JSON array, nothing else.

Notes:
{combined[:6000]}
"""
                    result = call_gemini(prompt)
                    try:
                        clean = re.sub(r'```json|```', '', result).strip()
                        cards = json.loads(clean)
                        st.session_state.flashcards = cards
                        st.success(f"✅ {len(cards)} flashcards created! Go to 🃏 Flashcards tab.")
                    except Exception:
                        st.error("Could not parse flashcards. Try again.")

        with col3:
            if st.button("🗂️ Auto-fill Question Bank", use_container_width=True):
                with st.spinner("Generating questions from your notes..."):
                    prompt = f"""
{student_context()}
Generate 20 exam questions from these notes, calibrated for this student's course, branch and semester.
For each question use this format:
Q1. [Question text]
Answer: [Answer]
Explanation: [Brief explanation]
Bloom: [Bloom's level]
Difficulty: [easy/medium/hard]
Marks: [1-10]
Type: [mcq/short/long/numerical]

Notes:
{combined[:6000]}
"""
                    result = call_gemini(prompt)
                    if result:
                        qs = parse_questions_from_text(result)
                        st.session_state.question_bank.extend(qs)
                        st.success(f"✅ {len(qs)} questions added to Question Bank!")

    else:
        st.markdown("""
        <div style="text-align:center;padding:3rem;color:#64748b;">
          <div style="font-size:3rem;margin-bottom:1rem;">📂</div>
          <div style="font-size:1rem;margin-bottom:0.5rem;">No files uploaded yet</div>
          <div style="font-size:0.8rem;">Upload your notes to unlock AI-powered question generation</div>
        </div>
        """, unsafe_allow_html=True)

# ── EXAM GENERATOR ──────────────────────────────────────────────────────────────
elif tab == "exam_gen":
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.8rem;margin-bottom:0.3rem;">
        📄 Exam Paper Generator
      </div>
      <div style="color:#64748b;font-size:0.9rem;">Generate complete exam papers with answer keys, Bloom's tags & difficulty distribution</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">⚙️ Paper Configuration</div>', unsafe_allow_html=True)
        subject = st.text_input("Subject Name", value=st.session_state.subject, placeholder="Data Structures")
        topic = st.text_input("Topic / Chapter", value=st.session_state.topic, placeholder="Binary Trees, Graphs")
        university = st.text_input("University", value=st.session_state.university, placeholder="Mumbai University")
        total_marks = st.slider("Total Marks", 20, 200, 100, 5)
        num_questions = st.slider("Number of Questions", 5, 50, 20)
        duration = st.slider("Exam Duration (minutes)", 30, 240, 180, 30)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🎯 Question Types & Difficulty</div>', unsafe_allow_html=True)
        difficulty = st.selectbox("Overall Difficulty", ["Mixed", "Easy", "Medium", "Hard", "Very Hard"])
        q_types = st.multiselect("Question Types",
            ["MCQ", "Short Answer", "Long Answer", "Numerical", "True/False", "Fill in the Blank", "Case Study"],
            default=["MCQ", "Short Answer", "Long Answer"])
        bloom_levels = st.multiselect("Bloom's Taxonomy Levels",
            ["Remember", "Understand", "Apply", "Analyse", "Evaluate", "Create"],
            default=["Remember", "Understand", "Apply", "Analyse"])
        include_answers = st.checkbox("Include Answer Key", value=True)
        include_explanations = st.checkbox("Include Explanations", value=True)
        use_notes = st.checkbox("Use Uploaded Notes as Syllabus", value=bool(st.session_state.notes_text))
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("⚡ Generate Exam Paper", use_container_width=True):
        notes_context = ""
        if use_notes and st.session_state.notes_text:
            notes_context = f"\nBase the questions strictly on these notes:\n{st.session_state.notes_text[:5000]}"

        prompt = f"""
You are an expert exam paper setter. Use the student profile to calibrate the paper precisely.
{student_context()}
Create a complete, professional exam paper:
- Subject: {subject}
- Topics: {topic}
- Total Marks: {total_marks}
- Number of Questions: {num_questions}
- Duration: {duration} minutes
- Difficulty: {difficulty}
- Question Types: {', '.join(q_types)}
- Bloom's Levels: {', '.join(bloom_levels)}

IMPORTANT: Tailor question complexity and content to the student's course, branch and semester.
For example, Maths for B.E. Computer Sem 1 differs from B.Pharm Sem 1 — use appropriate scope.

{notes_context}

Format each question EXACTLY as:
Q[N]. [Question text]
Type: [question type]
Marks: [marks]
Difficulty: [easy/medium/hard]
Bloom: [bloom's level]
{"Answer: [detailed answer]" if include_answers else ""}
{"Explanation: [explanation]" if include_explanations else ""}

After all questions, add a PAPER ANALYSIS section with:
- Difficulty distribution (% easy/medium/hard)
- Bloom's level coverage
- Topic coverage
- Marking scheme summary
- Important instructions for students

Be thorough and realistic. Make questions genuinely challenging and diverse.
"""
        with st.spinner("🔮 AI is crafting your exam paper..."):
            progress = st.progress(0)
            for i in range(0, 80, 10):
                time.sleep(0.1)
                progress.progress(i)
            result = call_gemini(prompt, max_tokens=6000)
            progress.progress(100)

        if result:
            st.session_state.generated_paper = {
                "content": result,
                "subject": subject,
                "topic": topic,
                "university": university,
                "marks": total_marks,
                "duration": duration,
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            st.session_state.generation_count += 1
            qs = parse_questions_from_text(result)
            if qs:
                st.session_state.question_bank.extend(qs)

    if st.session_state.generated_paper:
        paper = st.session_state.generated_paper
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card" style="margin-bottom:1rem;">
          <div style="display:flex;justify-content:space-between;align-items:start;flex-wrap:wrap;gap:1rem;">
            <div>
              <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;">
                📋 {paper['subject']} — Exam Paper
              </div>
              <div style="color:#64748b;font-size:0.82rem;margin-top:4px;">
                🏫 {paper['university']} &nbsp;|&nbsp; 📊 {paper['marks']} Marks &nbsp;|&nbsp;
                ⏱️ {paper['duration']} min &nbsp;|&nbsp; 🕐 Generated {paper['generated_at']}
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📄 View Full Exam Paper", expanded=True):
            st.markdown(f"""
            <div style="background:var(--surface2);border-radius:16px;padding:1.5rem;
                        font-family:'DM Mono',monospace;font-size:0.82rem;line-height:1.9;
                        white-space:pre-wrap;color:#cbd5e1;border:1px solid var(--border);">
{paper['content']}
            </div>
            """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.download_button("📥 Download TXT", data=paper["content"],
                file_name=f"exam_{paper['subject'].replace(' ','_')}.txt",
                mime="text/plain", use_container_width=True)
        with c2:
            st.download_button("📥 Download JSON",
                data=json.dumps(paper, indent=2),
                file_name=f"exam_{paper['subject'].replace(' ','_')}.json",
                mime="application/json", use_container_width=True)

# ── QUESTION BANK ───────────────────────────────────────────────────────────────
elif tab == "question_bank":
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.8rem;margin-bottom:0.3rem;">
        🗂️ Question Bank
      </div>
      <div style="color:#64748b;font-size:0.9rem;">Your personal collection — Expected Questions & Sample Papers</div>
    </div>
    """, unsafe_allow_html=True)

    bank_tab, sample_tab = st.tabs(["🎯 Expected Question Bank", "📋 Sample Question Papers"])

    with bank_tab:
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("➕ Generate More Questions", use_container_width=True):
                subj = st.session_state.subject or "General"
                topic = st.session_state.topic or "Mixed Topics"
                notes_ctx = f"\nFrom these notes:\n{st.session_state.notes_text[:4000]}" if st.session_state.notes_text else ""
                prompt = f"""
{student_context()}
Generate 15 expected exam questions tailored for this student's course, branch and semester.
Focus on questions MOST LIKELY to appear for their specific program — not generic questions.{notes_ctx}

Q[N]. [Question]
Answer: [Answer]
Explanation: [Explanation]
Bloom: [Level]
Difficulty: [easy/medium/hard]
Marks: [1-10]
Type: [mcq/short/long]
"""
                with st.spinner("Generating expected questions..."):
                    result = call_gemini(prompt)
                    if result:
                        qs = parse_questions_from_text(result)
                        st.session_state.question_bank.extend(qs)
                        st.success(f"✅ {len(qs)} questions added!")
                        st.rerun()
        with col2:
            if st.button("🗑️ Clear Bank", use_container_width=True):
                st.session_state.question_bank = []
                st.rerun()

        if not st.session_state.question_bank:
            st.markdown("""
            <div style="text-align:center;padding:3rem;color:#64748b;">
              <div style="font-size:3rem;margin-bottom:1rem;">🗂️</div>
              <div>No questions yet. Generate questions from the Exam Generator or upload your notes!</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                filter_diff = st.selectbox("Filter by Difficulty",
                    ["All", "Easy", "Medium", "Hard"], key="filter_diff")
            with fc2:
                filter_type = st.selectbox("Filter by Type",
                    ["All", "mcq", "short", "long", "numerical"], key="filter_type")
            with fc3:
                filter_bloom = st.selectbox("Filter by Bloom's",
                    ["All", "Remember", "Understand", "Apply", "Analyse", "Evaluate", "Create"],
                    key="filter_bloom")

            show_answers = st.checkbox("Show Answers & Explanations", value=True)

            filtered = st.session_state.question_bank
            if filter_diff != "All":
                filtered = [q for q in filtered if q.get("difficulty","").lower() == filter_diff.lower()]
            if filter_type != "All":
                filtered = [q for q in filtered if q.get("type","").lower() == filter_type.lower()]
            if filter_bloom != "All":
                filtered = [q for q in filtered if filter_bloom.lower() in q.get("bloom","").lower()]

            st.markdown(f"""
            <div style="font-family:'DM Mono',monospace;font-size:0.72rem;color:#64748b;
                        letter-spacing:1px;margin-bottom:1rem;">
              SHOWING {len(filtered)} OF {len(st.session_state.question_bank)} QUESTIONS
            </div>
            """, unsafe_allow_html=True)

            for i, q in enumerate(filtered[:50]):
                render_question_card(q, show_answers, i)

    with sample_tab:
        if st.button("📋 Generate Sample Question Paper", use_container_width=True):
            subj = st.session_state.subject or "General"
            uni = st.session_state.university or "University"
            notes_ctx = f"\nBased on:\n{st.session_state.notes_text[:4000]}" if st.session_state.notes_text else ""
            prompt = f"""
{student_context()}
Create a COMPLETE sample question paper that looks like an ACTUAL university exam paper.
Calibrate question depth and terminology to the student's course and semester level.{notes_ctx}

Include:
- Paper header with university name, course, branch, subject, marks, duration, instructions
- Section A: MCQ (20 marks)
- Section B: Short answer (30 marks)
- Section C: Long answer (50 marks)

With answer key at the end. Make it realistic and comprehensive.

Q[N]. [Question]
Answer: [Answer]
Explanation: [Explanation]
Bloom: [Level]
Difficulty: [easy/medium/hard]
Marks: [marks]
Type: [type]
"""
            with st.spinner("Generating sample paper..."):
                result = call_gemini(prompt, max_tokens=6000)
                if result:
                    st.session_state.generated_paper = {
                        "content": result, "subject": subj,
                        "topic": "Mixed", "university": uni,
                        "marks": 100, "duration": 180,
                        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }
                    st.success("Sample paper generated!")
                    st.rerun()

        if st.session_state.generated_paper:
            paper = st.session_state.generated_paper
            st.markdown(f"""
            <div class="card">
              <div class="card-title">📋 Sample Paper — {paper.get('subject','')}</div>
              <div style="color:#64748b;font-size:0.8rem;">
                {paper.get('university','')} | {paper.get('marks','')} Marks | Generated {paper.get('generated_at','')}
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:var(--surface2);border-radius:16px;padding:1.5rem;
                        font-family:'DM Mono',monospace;font-size:0.8rem;line-height:1.9;
                        white-space:pre-wrap;color:#cbd5e1;border:1px solid var(--border);
                        max-height:600px;overflow-y:auto;">
{paper['content']}
            </div>
            """, unsafe_allow_html=True)
            st.download_button("📥 Download Sample Paper",
                data=paper["content"],
                file_name=f"sample_{paper['subject'].replace(' ','_')}.txt",
                mime="text/plain", use_container_width=True)

# ── FLASHCARDS ──────────────────────────────────────────────────────────────────
elif tab == "flashcards":
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.8rem;margin-bottom:0.3rem;">
        🃏 Smart Flashcards
      </div>
      <div style="color:#64748b;font-size:0.9rem;">Flip to reveal — rapid revision for key concepts, formulas & definitions</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.flashcards:
        col1, col2 = st.columns(2)
        with col1:
            custom_topic = st.text_input("Topic for flashcards", placeholder="e.g. Binary Trees")
        with col2:
            num_cards = st.slider("Number of cards", 5, 30, 15)

        if st.button("🃏 Generate Flashcards", use_container_width=True):
            subj = st.session_state.subject or custom_topic or "General"
            notes_ctx = f"\nFrom these notes:\n{st.session_state.notes_text[:4000]}" if st.session_state.notes_text else ""
            prompt = f"""
{student_context()}
Create {num_cards} flashcards for revision, pitched at the right level for this student's course and semester.{notes_ctx}
Return ONLY a JSON array:
[
  {{"front": "Question or term", "back": "Answer or definition", "category": "subtopic"}},
  ...
]
No markdown, no extra text. Only valid JSON.
"""
            with st.spinner("Creating flashcards..."):
                result = call_gemini(prompt)
                try:
                    clean = re.sub(r'```json|```', '', result).strip()
                    cards = json.loads(clean)
                    st.session_state.flashcards = cards
                    st.success(f"✅ {len(cards)} flashcards ready!")
                    st.rerun()
                except Exception:
                    st.error("Could not parse. Try again.")
    else:
        cards = st.session_state.flashcards

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if "card_idx" not in st.session_state:
                st.session_state.card_idx = 0
            if "card_flipped" not in st.session_state:
                st.session_state.card_flipped = False

            idx = st.session_state.card_idx % len(cards)
            card = cards[idx]
            flipped = st.session_state.card_flipped

            st.markdown(f"""
            <div style="text-align:center;margin-bottom:0.5rem;">
              <span style="font-family:'DM Mono',monospace;font-size:0.7rem;
                           color:#64748b;letter-spacing:1px;">
                CARD {idx+1} / {len(cards)} &nbsp;·&nbsp; {card.get('category','General').upper()}
              </span>
            </div>
            """, unsafe_allow_html=True)

            face_content = card['back'] if flipped else card['front']
            face_emoji = "✅" if flipped else "❓"
            face_color = "rgba(16,185,129,0.12)" if flipped else "var(--surface)"
            face_border = "rgba(16,185,129,0.3)" if flipped else "var(--border)"
            face_label = "ANSWER" if flipped else "QUESTION — Click Flip to reveal"

            st.markdown(f"""
            <div style="background:{face_color};border:2px solid {face_border};
                        border-radius:24px;padding:2.5rem;text-align:center;
                        min-height:200px;display:flex;flex-direction:column;
                        align-items:center;justify-content:center;gap:1rem;
                        transition:all 0.4s ease;margin-bottom:1rem;">
              <div style="font-size:2.5rem;">{face_emoji}</div>
              <div style="font-family:'DM Mono',monospace;font-size:0.65rem;
                           color:#64748b;letter-spacing:2px;">{face_label}</div>
              <div style="font-family:'Syne',sans-serif;font-size:1.1rem;
                           font-weight:600;color:#e2e8f0;line-height:1.6;">
                {face_content}
              </div>
            </div>
            """, unsafe_allow_html=True)

            b1, b2, b3 = st.columns(3)
            with b1:
                if st.button("⬅️ Previous", use_container_width=True):
                    st.session_state.card_idx = (idx - 1) % len(cards)
                    st.session_state.card_flipped = False
                    st.rerun()
            with b2:
                flip_label = "🔄 Flip Back" if flipped else "🔄 Flip Card"
                if st.button(flip_label, use_container_width=True):
                    st.session_state.card_flipped = not flipped
                    st.rerun()
            with b3:
                if st.button("➡️ Next", use_container_width=True):
                    st.session_state.card_idx = (idx + 1) % len(cards)
                    st.session_state.card_flipped = False
                    st.rerun()

        st.progress((idx + 1) / len(cards))
        st.markdown(f"""
        <div style="text-align:center;font-size:0.75rem;color:#64748b;margin-top:0.5rem;">
          {idx+1} of {len(cards)} cards reviewed
        </div>
        """, unsafe_allow_html=True)

        if st.button("🗑️ Clear Flashcards & Regenerate"):
            st.session_state.flashcards = []
            st.session_state.card_idx = 0
            st.session_state.card_flipped = False
            st.rerun()

# ── TIMED PRACTICE ──────────────────────────────────────────────────────────────
elif tab == "timer":
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.8rem;margin-bottom:0.3rem;">
        ⏱️ Timed Practice Mode
      </div>
      <div style="color:#64748b;font-size:0.9rem;">Simulate real exam pressure. Answer questions against the clock.</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.quiz_mode:
        col1, col2 = st.columns(2)
        with col1:
            num_qs = st.slider("Number of questions", 5, 30, 10)
            time_per_q = st.slider("Minutes per question", 1, 10, 3)
        with col2:
            quiz_diff = st.selectbox("Difficulty", ["Mixed", "Easy", "Medium", "Hard"])
            use_bank = st.checkbox("Use my Question Bank", value=bool(st.session_state.question_bank))

        if st.button("🚀 Start Timed Practice", use_container_width=True):
            if use_bank and st.session_state.question_bank:
                pool = st.session_state.question_bank.copy()
                random.shuffle(pool)
                qs = pool[:num_qs]
            elif st.session_state.api_key:
                subj = st.session_state.subject or "General Knowledge"
                notes_ctx = f"\nFrom:\n{st.session_state.notes_text[:3000]}" if st.session_state.notes_text else ""
                prompt = f"""
{student_context()}
Generate {num_qs} {quiz_diff} difficulty MCQ/short questions calibrated for this student's course, branch and semester.{notes_ctx}
Each question MUST have exactly 4 options (A, B, C, D) if MCQ.
Format:
Q[N]. [Question]
A) option B) option C) option D) option
Answer: [letter or text]
Explanation: [explanation]
Bloom: [level]
Difficulty: [{quiz_diff.lower() if quiz_diff != 'Mixed' else 'medium'}]
Marks: [1-5]
Type: [mcq/short]
"""
                with st.spinner("Preparing your practice set..."):
                    result = call_gemini(prompt)
                    qs = parse_questions_from_text(result) if result else []
            else:
                st.error("Either add questions to your bank or enter API key.")
                qs = []

            if qs:
                st.session_state.quiz_questions = qs
                st.session_state.quiz_mode = True
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answered = False
                total_time = num_qs * time_per_q * 60
                st.session_state.timer_seconds = total_time
                st.session_state.timer_start = time.time()
                st.rerun()
    else:
        qs = st.session_state.quiz_questions
        idx = st.session_state.quiz_index

        elapsed = time.time() - (st.session_state.timer_start or time.time())
        remaining = max(0, st.session_state.timer_seconds - int(elapsed))
        mins = remaining // 60
        secs = remaining % 60

        timer_color = "#22d3ee"
        if remaining < 300:
            timer_color = "#f59e0b"
        if remaining < 60:
            timer_color = "#ef4444"

        st.markdown(f"""
        <div style="text-align:center;margin-bottom:1.5rem;">
          <div style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;
                       color:{timer_color};text-shadow:0 0 30px {timer_color}40;">
            {mins:02d}:{secs:02d}
          </div>
          <div style="font-family:'DM Mono',monospace;font-size:0.7rem;color:#64748b;
                       letter-spacing:2px;margin-top:4px;">TIME REMAINING</div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(remaining / st.session_state.timer_seconds if st.session_state.timer_seconds > 0 else 0)

        if remaining == 0:
            st.error("⏰ Time's up!")
            st.session_state.quiz_mode = False
            st.rerun()

        if idx < len(qs):
            q = qs[idx]
            st.markdown(f"""
            <div style="background:var(--surface);border:1px solid var(--border);
                        border-radius:18px;padding:1.5rem;margin:1rem 0;">
              <div style="font-family:'DM Mono',monospace;font-size:0.7rem;color:#64748b;
                           letter-spacing:1px;margin-bottom:0.8rem;">
                QUESTION {idx+1} / {len(qs)} &nbsp;·&nbsp;
                {q.get('marks',2)} MARKS &nbsp;·&nbsp;
                {q.get('difficulty','medium').upper()}
              </div>
              <div style="font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:600;
                           line-height:1.6;color:#e2e8f0;">
                {q.get('question','')}
              </div>
            </div>
            """, unsafe_allow_html=True)

            user_answer = st.text_area("Your Answer:", height=100, key=f"ans_{idx}")

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("✅ Submit Answer", use_container_width=True) and not st.session_state.quiz_answered:
                    st.session_state.quiz_answered = True
                    if user_answer.strip():
                        st.session_state.quiz_score += q.get("marks", 2)
            with c2:
                if st.button("⏭️ Skip Question", use_container_width=True):
                    st.session_state.quiz_index += 1
                    st.session_state.quiz_answered = False
                    st.rerun()
            with c3:
                if st.button("🚫 End Quiz", use_container_width=True):
                    st.session_state.quiz_mode = False
                    st.rerun()

            if st.session_state.quiz_answered:
                st.success(f"✅ **Correct Answer:** {q.get('answer','')}")
                if q.get("explanation"):
                    st.info(f"💡 {q.get('explanation','')}")
                if st.button("➡️ Next Question", use_container_width=True):
                    st.session_state.quiz_index += 1
                    st.session_state.quiz_answered = False
                    st.rerun()
        else:
            total_possible = sum(q.get("marks", 2) for q in qs)
            score = st.session_state.quiz_score
            pct = int(score / total_possible * 100) if total_possible > 0 else 0
            grade = "A+" if pct >= 90 else "A" if pct >= 80 else "B" if pct >= 70 else "C" if pct >= 60 else "D" if pct >= 50 else "F"

            st.markdown(f"""
            <div style="text-align:center;padding:3rem;background:var(--surface);
                        border-radius:24px;border:1px solid var(--border);margin:1rem 0;">
              <div style="font-size:4rem;margin-bottom:1rem;">🎉</div>
              <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;
                           background:linear-gradient(135deg,#6366f1,#22d3ee);
                           -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                           background-clip:text;">
                Practice Complete!
              </div>
              <div style="margin:1.5rem 0;">
                <div style="font-size:4rem;font-family:'Syne',sans-serif;font-weight:800;
                             color:#22d3ee;">{grade}</div>
                <div style="font-size:1.2rem;color:#94a3b8;margin-top:0.5rem;">
                  {score} / {total_possible} marks ({pct}%)
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.quiz_mode = False
                st.rerun()

# ── PYQ ANALYSER ────────────────────────────────────────────────────────────────
elif tab == "pyq":
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.8rem;margin-bottom:0.3rem;">
        📚 PYQ Analyser — Past Year Questions
      </div>
      <div style="color:#64748b;font-size:0.9rem;">
        AI analyses patterns from past year papers of your university to predict what's coming next
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        uni = st.text_input("University Name", value=st.session_state.university,
                            placeholder="Mumbai University / VTU / SPPU...")
        subj = st.text_input("Subject", value=st.session_state.subject,
                             placeholder="Data Structures and Algorithms")
    with col2:
        exam_type = st.selectbox("Exam Type", ["Semester End Exam", "Mid-Term", "Internal", "Entrance"])
        years = st.slider("Years of PYQ to analyse", 2, 10, 5)

    uploaded_pyq = st.file_uploader("Upload PYQ Papers (optional, for better analysis)",
                                     type=["pdf", "txt", "docx"],
                                     accept_multiple_files=True,
                                     key="pyq_upload")

    pyq_context = ""
    if uploaded_pyq:
        for f in uploaded_pyq:
            pyq_context += f"\n\n--- {f.name} ---\n{extract_text_from_file(f)}"

    if st.button("🔍 Analyse PYQ Patterns", use_container_width=True):
        notes_ctx = f"\nStudent notes:\n{st.session_state.notes_text[:3000]}" if st.session_state.notes_text else ""
        pyq_ctx = f"\nActual PYQ papers:\n{pyq_context[:4000]}" if pyq_context else ""
        prompt = f"""
You are an expert in university exam patterns.
{student_context()}
Analyse {years} years of PYQ for {subj} ({exam_type}) and provide:

1. **MOST REPEATED TOPICS** — ranked by frequency, specific to this course & branch
2. **QUESTION TYPE DISTRIBUTION** — % MCQ, short, long, numerical
3. **DIFFICULTY TREND** — is it getting harder/easier over the years?
4. **HIGH-PROBABILITY QUESTIONS FOR NEXT EXAM** — 10 specific questions likely to appear for this course/sem
5. **NEVER-ASKED TOPICS** — in syllabus but rarely appear
6. **MARKING SCHEME INSIGHTS** — how marks are typically distributed
7. **LAST YEAR IMPORTANT QUESTIONS** — recreated from memory
8. **STUDY STRATEGY** — tailored to this student's course, branch and semester

{notes_ctx}
{pyq_ctx}

Be specific. Remember: {st.session_state.course or 'a student'} in {st.session_state.branch or 'their branch'} has a different syllabus scope than other programs.
"""
        with st.spinner(f"🔍 Analysing {years} years of {uni} PYQ patterns..."):
            result = call_gemini(prompt, max_tokens=5000)
            if result:
                st.markdown(f"""
                <div style="background:var(--surface);border:1px solid var(--border);
                            border-radius:18px;padding:1.5rem;margin-top:1rem;
                            font-size:0.88rem;line-height:1.8;color:#cbd5e1;
                            white-space:pre-wrap;">
{result}
                </div>
                """, unsafe_allow_html=True)
                st.download_button("📥 Download PYQ Analysis",
                    data=result, file_name="pyq_analysis.txt",
                    mime="text/plain", use_container_width=True)

# ── IMP TOPICS ──────────────────────────────────────────────────────────────────
elif tab == "imp_topics":
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.8rem;margin-bottom:0.3rem;">
        🔥 Important Topics
      </div>
      <div style="color:#64748b;font-size:0.9rem;">
        AI-identified high-priority topics most likely to appear in your exam
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.imp_topics:
        col1, col2 = st.columns(2)
        with col1:
            subj_input = st.text_input("Subject", value=st.session_state.subject, placeholder="Data Structures")
        with col2:
            uni_input = st.text_input("University", value=st.session_state.university, placeholder="Mumbai University")

        if st.button("🔥 Identify Important Topics", use_container_width=True):
            notes_ctx = f"\nBased on these notes:\n{st.session_state.notes_text[:5000]}" if st.session_state.notes_text else ""
            prompt = f"""
Act as an expert exam coach.
{student_context()}

Identify and rank the TOP 20 most important topics for this student's exam.
CRITICAL: Tailor topics to their specific course, branch and semester — not a generic list.
For example, Applied Maths for B.E. Sem 1 is very different from B.Pharm Sem 1.{notes_ctx}

For each topic provide:
1. Topic name & subtopics (relevant to their course/branch)
2. Importance level: 🔴 MUST KNOW / 🟡 IMPORTANT / 🟢 GOOD TO KNOW
3. Expected marks weightage for their exam pattern
4. Most likely question format
5. Key formulas/concepts to memorise
6. Difficulty level
7. Quick study tip specific to their level

Also provide:
- 5 topics to absolutely NOT skip
- Predicted question from each top 5 topic
- Study time allocation recommendation

Format clearly with emojis and structure.
"""
            with st.spinner("🔥 Identifying critical exam topics..."):
                result = call_gemini(prompt, max_tokens=5000)
                if result:
                    st.session_state.imp_topics = result
                    st.rerun()
    else:
        st.markdown(f"""
        <div style="background:var(--surface);border:1px solid var(--border);
                    border-radius:18px;padding:1.5rem;font-size:0.88rem;
                    line-height:1.9;color:#cbd5e1;white-space:pre-wrap;
                    max-height:700px;overflow-y:auto;">
{st.session_state.imp_topics}
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.download_button("📥 Download Important Topics",
                data=st.session_state.imp_topics,
                file_name="important_topics.txt", mime="text/plain",
                use_container_width=True)
        with c2:
            if st.button("🔄 Regenerate", use_container_width=True):
                st.session_state.imp_topics = ""
                st.rerun()

# ── ANALYTICS ───────────────────────────────────────────────────────────────────
elif tab == "analytics":
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
      <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.8rem;margin-bottom:0.3rem;">
        📈 Paper Analytics
      </div>
      <div style="color:#64748b;font-size:0.9rem;">
        Insights into your question bank, difficulty distribution & Bloom's coverage
      </div>
    </div>
    """, unsafe_allow_html=True)

    qs = st.session_state.question_bank
    if not qs:
        st.info("No questions yet! Generate some questions first to see analytics.")
    else:
        total = len(qs)
        easy = sum(1 for q in qs if q.get("difficulty","").lower() == "easy")
        medium = sum(1 for q in qs if q.get("difficulty","").lower() == "medium")
        hard = sum(1 for q in qs if q.get("difficulty","").lower() == "hard")
        total_marks = sum(q.get("marks", 2) for q in qs)

        st.markdown(f"""
        <div class="analysis-grid">
          <div class="analysis-card">
            <div class="analysis-value" style="color:#22d3ee;">{total}</div>
            <div class="analysis-label">Total Questions</div>
          </div>
          <div class="analysis-card">
            <div class="analysis-value" style="color:#10b981;">{easy}</div>
            <div class="analysis-label">Easy</div>
          </div>
          <div class="analysis-card">
            <div class="analysis-value" style="color:#f59e0b;">{medium}</div>
            <div class="analysis-label">Medium</div>
          </div>
          <div class="analysis-card">
            <div class="analysis-value" style="color:#ef4444;">{hard}</div>
            <div class="analysis-label">Hard</div>
          </div>
          <div class="analysis-card">
            <div class="analysis-value" style="color:#a78bfa;">{total_marks}</div>
            <div class="analysis-label">Total Marks</div>
          </div>
          <div class="analysis-card">
            <div class="analysis-value" style="color:#f472b6;">{len(st.session_state.flashcards)}</div>
            <div class="analysis-label">Flashcards</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        bloom_counts = {}
        for q in qs:
            b = q.get("bloom", "Unknown")
            for level in ["Remember","Understand","Apply","Analyse","Evaluate","Create"]:
                if level.lower() in b.lower():
                    bloom_counts[level] = bloom_counts.get(level, 0) + 1
                    break

        if bloom_counts:
            st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-family:'Syne',sans-serif;font-weight:700;margin-bottom:1rem;">
              🧠 Bloom's Taxonomy Coverage
            </div>
            """, unsafe_allow_html=True)
            bloom_order = ["Remember","Understand","Apply","Analyse","Evaluate","Create"]
            bloom_colors = ["#6366f1","#22d3ee","#10b981","#f59e0b","#ef4444","#a78bfa"]
            for i, level in enumerate(bloom_order):
                count = bloom_counts.get(level, 0)
                pct = int(count / total * 100) if total > 0 else 0
                color = bloom_colors[i]
                st.markdown(f"""
                <div style="margin-bottom:12px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                    <span style="font-family:'DM Mono',monospace;font-size:0.75rem;color:#94a3b8;">{level}</span>
                    <span style="font-family:'DM Mono',monospace;font-size:0.75rem;color:#64748b;">{count} questions ({pct}%)</span>
                  </div>
                  <div style="background:var(--surface2);border-radius:100px;height:8px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{color};border-radius:100px;
                                transition:width 1s ease;box-shadow:0 0 12px {color}60;"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        type_counts = {}
        for q in qs:
            t = q.get("type", "unknown").lower()
            type_counts[t] = type_counts.get(t, 0) + 1

        if type_counts:
            st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-family:'Syne',sans-serif;font-weight:700;margin-bottom:1rem;">
              📝 Question Type Distribution
            </div>
            """, unsafe_allow_html=True)
            cols = st.columns(len(type_counts))
            for i, (typ, cnt) in enumerate(type_counts.items()):
                with cols[i % len(cols)]:
                    pct = int(cnt / total * 100)
                    st.markdown(f"""
                    <div class="analysis-card">
                      <div class="analysis-value" style="color:#22d3ee;font-size:1.5rem;">{pct}%</div>
                      <div class="analysis-label">{typ.title()}</div>
                      <div style="font-size:0.7rem;color:#64748b;margin-top:2px;">{cnt} questions</div>
                    </div>
                    """, unsafe_allow_html=True)

        if st.button("🤖 Get AI Insights on Your Prep", use_container_width=True):
            prompt = f"""
{student_context()}
Question bank analytics for this student:
- Total questions: {total}
- Easy: {easy} ({int(easy/total*100) if total else 0}%)
- Medium: {medium} ({int(medium/total*100) if total else 0}%)
- Hard: {hard} ({int(hard/total*100) if total else 0}%)
- Bloom's coverage: {bloom_counts}
- Question types: {type_counts}
- Flashcards created: {len(st.session_state.flashcards)}

Provide insights tailored to their course and semester level:
1. Assessment of their preparation level
2. What areas they're strong in
3. Gaps in their preparation (specific to their course/branch syllabus)
4. Specific recommendations to improve
5. Suggested study plan for the next 7 days
6. Confidence score (0-100) for their exam readiness

Be encouraging but honest.
"""
            with st.spinner("Analysing your preparation..."):
                result = call_gemini(prompt)
                if result:
                    st.markdown(f"""
                    <div style="background:var(--surface);border:1px solid var(--border);
                                border-radius:18px;padding:1.5rem;margin-top:1rem;
                                font-size:0.88rem;line-height:1.8;color:#cbd5e1;">
{result}
                    </div>
                    """, unsafe_allow_html=True)

# ── FOOTER ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:3rem 1rem 1rem;
            border-top:1px solid rgba(99,102,241,0.12);margin-top:3rem;">
  <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:1rem;
               background:linear-gradient(135deg,#6366f1,#22d3ee);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;margin-bottom:0.4rem;">⚡ ExamForge AI</div>
  <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#475569;
               letter-spacing:1.5px;">YOUR FINAL PREP PLATFORM · POWERED BY GOOGLE GEMINI</div>
</div>
""", unsafe_allow_html=True)