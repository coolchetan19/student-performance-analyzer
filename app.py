import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.predictor import generate_report
import json

# ── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

/* ---- Base ---- */
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

/* ---- Background ---- */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
    min-height: 100vh;
}

/* ---- Hero Header ---- */
.hero-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    border-radius: 20px;
    padding: 40px 48px;
    margin-bottom: 32px;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    color: white;
    margin: 0 0 8px 0;
    text-shadow: 0 2px 20px rgba(0,0,0,0.3);
}
.hero-subtitle {
    color: rgba(255,255,255,0.85);
    font-size: 1.05rem;
    font-weight: 400;
    margin: 0;
}

/* ---- Cards ---- */
.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
}
.card-title {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.5);
    margin-bottom: 12px;
}

/* ---- Metric Cards ---- */
.metric-card {
    background: rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-2px); }
.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: white;
    line-height: 1;
}
.metric-label {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.55);
    margin-top: 6px;
    font-weight: 500;
    letter-spacing: 0.05em;
}

/* ---- Category Badge ---- */
.badge-excellent { background: linear-gradient(135deg, #11998e, #38ef7d); }
.badge-good      { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.badge-average   { background: linear-gradient(135deg, #f093fb, #f5576c); }
.badge-weak      { background: linear-gradient(135deg, #f7971e, #ffd200); }

.perf-badge {
    display: inline-block;
    padding: 10px 28px;
    border-radius: 50px;
    font-size: 1.4rem;
    font-weight: 700;
    color: white;
    letter-spacing: 0.03em;
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}

/* ---- Progress Bar ---- */
.prog-wrap { margin-bottom: 14px; }
.prog-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    color: rgba(255,255,255,0.75);
    margin-bottom: 5px;
}
.prog-bar-bg {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    height: 10px;
    overflow: hidden;
}
.prog-bar-fill {
    height: 100%;
    border-radius: 20px;
    transition: width 0.5s ease;
}

/* ---- Strength / Weakness pills ---- */
.pill-strength {
    display: inline-block;
    background: rgba(56, 239, 125, 0.15);
    border: 1px solid rgba(56, 239, 125, 0.4);
    color: #38ef7d;
    padding: 5px 14px;
    border-radius: 30px;
    font-size: 0.82rem;
    font-weight: 600;
    margin: 4px 4px 4px 0;
}
.pill-weakness {
    display: inline-block;
    background: rgba(245, 87, 108, 0.15);
    border: 1px solid rgba(245, 87, 108, 0.4);
    color: #f5576c;
    padding: 5px 14px;
    border-radius: 30px;
    font-size: 0.82rem;
    font-weight: 600;
    margin: 4px 4px 4px 0;
}

/* ---- Suggestion items ---- */
.suggestion-item {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #667eea;
    padding: 10px 16px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 10px;
    color: rgba(255,255,255,0.85);
    font-size: 0.9rem;
    line-height: 1.5;
}

/* ---- Sidebar ---- */
section[data-testid="stSidebar"] {
    background: rgba(15, 12, 41, 0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
.sidebar-section-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.4) !important;
    margin: 20px 0 10px 0;
}

/* ---- Footer ---- */
.footer {
    background: rgba(255,255,255,0.03);
    border-top: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 20px 28px;
    margin-top: 40px;
    text-align: center;
    color: rgba(255,255,255,0.45);
    font-size: 0.82rem;
    line-height: 1.8;
}
.footer a { color: #667eea !important; text-decoration: none; }
.footer a:hover { color: #f093fb !important; }

/* ---- Streamlit overrides ---- */
.stSlider > div > div { background: transparent !important; }
label { color: rgba(255,255,255,0.75) !important; }
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 14px 36px;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 700;
    width: 100%;
    letter-spacing: 0.05em;
    box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4);
    transition: all 0.2s;
    cursor: pointer;
}
.stButton > button:hover {
    box-shadow: 0 12px 40px rgba(102, 126, 234, 0.6);
    transform: translateY(-1px);
}
div[data-testid="stSelectbox"] > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# ── Hero Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🎓 Student Performance Analyzer</div>
    <p class="hero-subtitle">ML-powered academic intelligence · Predict · Analyze · Improve</p>
</div>
""", unsafe_allow_html=True)


# ── Sidebar Inputs ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-section-title">⚙️ Model Selection</div>', unsafe_allow_html=True)
    model_choice = st.selectbox(
        "Classifier",
        ['random_forest', 'xgboost', 'logistic_regression'],
        format_func=lambda x: {'random_forest': '🌲 Random Forest', 'xgboost': '⚡ XGBoost', 'logistic_regression': '📊 Logistic Regression'}[x]
    )

    st.markdown('<div class="sidebar-section-title">📋 Academic Performance</div>', unsafe_allow_html=True)
    attendance = st.slider("Attendance (%)", 0, 100, 75)
    midterm = st.slider("Midterm Marks", 0, 100, 65)
    assignment = st.slider("Assignment Score", 0, 100, 70)
    lab = st.slider("Lab Performance", 0, 100, 68)

    st.markdown('<div class="sidebar-section-title">📚 Subject-wise Marks</div>', unsafe_allow_html=True)
    math = st.slider("Mathematics", 0, 100, 72)
    programming = st.slider("Programming", 0, 100, 60)
    dbms = st.slider("DBMS", 0, 100, 65)
    english = st.slider("English", 0, 100, 70)
    os_score = st.slider("Operating Systems", 0, 100, 63)

    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🔍 Analyze Student")


# ── Load metrics ─────────────────────────────────────────────────────────────
@st.cache_data
def load_metrics():
    with open('models/metrics.json') as f:
        return json.load(f)

metrics = load_metrics()


# ── Default state ─────────────────────────────────────────────────────────────
if not analyze_btn:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['random_forest']*100:.1f}%</div>
            <div class="metric-label">Random Forest Accuracy</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['xgboost']*100:.1f}%</div>
            <div class="metric-label">XGBoost Accuracy</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['logistic_regression']*100:.1f}%</div>
            <div class="metric-label">Logistic Regression Accuracy</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="margin-top:28px; text-align:center; padding: 48px;">
        <div style="font-size:3rem; margin-bottom:16px;">📊</div>
        <div style="color:rgba(255,255,255,0.7); font-size:1.05rem; margin-bottom:8px;">Ready to Analyze</div>
        <div style="color:rgba(255,255,255,0.4); font-size:0.88rem;">Fill in student data in the sidebar and click <strong>Analyze Student</strong> to generate a full performance report.</div>
    </div>
    """, unsafe_allow_html=True)

else:
    # ── Run prediction ────────────────────────────────────────────────────────
    student_data = {
        'attendance': attendance,
        'midterm_marks': midterm,
        'assignment_score': assignment,
        'lab_performance': lab,
        'mathematics': math,
        'programming': programming,
        'dbms': dbms,
        'english': english,
        'operating_systems': os_score,
    }

    with st.spinner("Analyzing student data..."):
        report = generate_report(student_data, model_choice)

    cat = report['category']
    badge_cls = f"badge-{cat.lower()}"

    # ── Row 1: Summary ────────────────────────────────────────────────────────
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size:1.6rem;">{report['overall_score']}</div>
            <div class="metric-label">Overall Score / 100</div>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size:1.6rem;">{report['attendance']}%</div>
            <div class="metric-label">Attendance</div>
        </div>""", unsafe_allow_html=True)
    with col_c:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size:1.6rem;">{report['consistency']}</div>
            <div class="metric-label">Consistency Score</div>
        </div>""", unsafe_allow_html=True)
    with col_d:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size:1.05rem;">{report['risk_level']}</div>
            <div class="metric-label">Risk Level</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: Category + Confidence + Subject Scores ─────────────────────────
    col_left, col_right = st.columns([1, 1.6])

    with col_left:
        st.markdown(f"""
        <div class="card" style="text-align:center; padding:32px;">
            <div class="card-title">Performance Category</div>
            <div class="perf-badge {badge_cls}">{cat}</div>
            <div style="margin-top:24px; color:rgba(255,255,255,0.5); font-size:0.8rem;">Model: {model_choice.replace('_', ' ').title()}</div>
        </div>""", unsafe_allow_html=True)

        # Confidence breakdown
        st.markdown('<div class="card"><div class="card-title">Model Confidence</div>', unsafe_allow_html=True)
        colors = {'Excellent': '#38ef7d', 'Good': '#00f2fe', 'Average': '#f093fb', 'Weak': '#ffd200'}
        for cls, pct in sorted(report['confidence'].items(), key=lambda x: -x[1]):
            color = colors.get(cls, '#667eea')
            st.markdown(f"""
            <div class="prog-wrap">
                <div class="prog-label"><span>{cls}</span><span>{pct}%</span></div>
                <div class="prog-bar-bg">
                    <div class="prog-bar-fill" style="width:{pct}%; background:{color};"></div>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="card"><div class="card-title">Subject-wise Performance</div>', unsafe_allow_html=True)
        subj_colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#38ef7d']
        for i, (subj, score) in enumerate(report['subject_scores'].items()):
            color = subj_colors[i % len(subj_colors)]
            st.markdown(f"""
            <div class="prog-wrap">
                <div class="prog-label"><span>{subj}</span><span>{score}/100</span></div>
                <div class="prog-bar-bg">
                    <div class="prog-bar-fill" style="width:{score}%; background:{color};"></div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Academic metrics
        for label, val, key in [
            ("Midterm Marks", report['midterm'], '#f5576c'),
            ("Assignment Score", report['assignment'], '#f093fb'),
            ("Lab Performance", report['lab'], '#4facfe'),
        ]:
            st.markdown(f"""
            <div class="prog-wrap">
                <div class="prog-label"><span>{label}</span><span>{val}/100</span></div>
                <div class="prog-bar-bg">
                    <div class="prog-bar-fill" style="width:{val}%; background:{key};"></div>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 3: Strengths + Weaknesses ────────────────────────────────────────
    col_s, col_w = st.columns(2)
    with col_s:
        st.markdown('<div class="card"><div class="card-title">💪 Strengths</div>', unsafe_allow_html=True)
        if report['strengths']:
            pills = ''.join([f'<span class="pill-strength">✅ {s} ({sc})</span>' for s, sc in report['strengths']])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:rgba(255,255,255,0.4); font-size:0.88rem;">No subject scoring ≥75 yet.</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_w:
        st.markdown('<div class="card"><div class="card-title">⚠️ Weak Areas</div>', unsafe_allow_html=True)
        if report['weaknesses']:
            pills = ''.join([f'<span class="pill-weakness">❌ {s} ({sc})</span>' for s, sc in report['weaknesses']])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:rgba(255,255,255,0.4); font-size:0.88rem;">No critical weaknesses detected.</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 4: Suggestions ────────────────────────────────────────────────────
    st.markdown('<div class="card"><div class="card-title">🎯 Personalized Improvement Suggestions</div>', unsafe_allow_html=True)
    for suggestion in report['suggestions']:
        st.markdown(f'<div class="suggestion-item">{suggestion}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <strong style="color:rgba(255,255,255,0.7);">Student Performance Analyzer</strong> &nbsp;|&nbsp;
    Developed by <strong style="color:#667eea;">Chetan Kumar Sambhawani</strong> &nbsp;|&nbsp;
    <a href="https://github.com/coolchetan19" target="_blank">🐙 GitHub</a> &nbsp;|&nbsp;
    <a href="https://www.linkedin.com/in/chetan-kumar-sambhawani-b1b833326/" target="_blank">💼 LinkedIn</a>
    <br><span style="font-size:0.75rem; color:rgba(255,255,255,0.3);">Powered by Random Forest · XGBoost · Logistic Regression</span>
</div>
""", unsafe_allow_html=True)
