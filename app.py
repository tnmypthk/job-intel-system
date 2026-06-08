import streamlit as st
from dotenv import load_dotenv
import re
from gmail_helper import create_gmail_draft
from crewai import Crew, Process
from agents.jd_analyzer import create_jd_analyzer
from agents.company_researcher import create_company_researcher
from agents.skills_gap_scorer import create_skills_gap_scorer
from agents.resume_tailor import create_resume_tailor
from agents.interview_prep_writer import create_interview_prep_writer
from tasks.task_definitions import (
    create_jd_analysis_task,
    create_company_research_task,
    create_skills_gap_task,
    create_resume_tailor_task,
    create_interview_prep_task

)

load_dotenv()

st.set_page_config(page_title="Job Intel", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.html("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap" rel="stylesheet">
<style>
.stApp { background: #080C14; font-family: 'DM Sans', sans-serif; }
.main .block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }
#MainMenu, footer, .stDeployButton { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; }

h1,h2,h3 { font-family: 'Syne', sans-serif !important; letter-spacing: -0.02em; }

.stTextInput > label, .stTextArea > label {
    font-family: 'DM Mono', monospace !important; font-size: 11px !important;
    letter-spacing: 0.12em !important; text-transform: uppercase !important;
    color: #4B5563 !important; margin-bottom: 6px !important;
}

.stTextInput > div > div > input {
    background: #0F1623 !important; border: 1px solid #1E2A3A !important;
    color: #E2E8F0 !important; border-radius: 10px !important;
    padding: 12px 16px !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important; transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00D4AA !important;
    box-shadow: 0 0 0 3px rgba(0,212,170,0.1) !important;
}

.stTextArea > div > div > textarea {
    background: #0F1623 !important; border: 1px solid #1E2A3A !important;
    color: #E2E8F0 !important; border-radius: 10px !important;
    padding: 14px 16px !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important; line-height: 1.6 !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: #00D4AA !important;
    box-shadow: 0 0 0 3px rgba(0,212,170,0.1) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #00D4AA 0%, #0099CC 100%) !important;
    color: #080C14 !important; border: none !important; border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    font-size: 15px !important; letter-spacing: 0.02em !important;
    padding: 14px 28px !important; transition: all 0.25s !important;
    box-shadow: 0 4px 20px rgba(0,212,170,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(0,212,170,0.4) !important;
}
.stButton > button:disabled {
    background: #1E2A3A !important; color: #4B5563 !important;
    box-shadow: none !important; transform: none !important;
}

hr { border-color: #1E2A3A !important; margin: 2rem 0 !important; }

.stTabs [data-baseweb="tab-list"] {
    background: #0F1623 !important; border-radius: 12px !important;
    padding: 5px !important; gap: 4px !important;
    border: 1px solid #1E2A3A !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #6B7280 !important;
    border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important; font-weight: 500 !important;
    padding: 8px 16px !important; border: none !important; transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: #00D4AA !important; color: #080C14 !important; font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem !important; }

.stSuccess {
    background: rgba(0,212,170,0.08) !important;
    border: 1px solid rgba(0,212,170,0.3) !important;
    border-radius: 10px !important; color: #00D4AA !important;
}

.stMarkdown h1, .stMarkdown h2 {
    font-family: 'Syne', sans-serif !important; color: #E2E8F0 !important;
    border-bottom: 1px solid #1E2A3A !important;
    padding-bottom: 8px !important; margin-top: 1.5rem !important;
}
.stMarkdown h3 {
    font-family: 'Syne', sans-serif !important; color: #00D4AA !important;
    font-size: 13px !important; text-transform: uppercase !important;
    letter-spacing: 0.08em !important; margin-top: 1.5rem !important;
}
.stMarkdown p { color: #94A3B8 !important; line-height: 1.75 !important; font-size: 14px !important; }
.stMarkdown strong { color: #E2E8F0 !important; }
.stMarkdown li { color: #94A3B8 !important; font-size: 14px !important; line-height: 1.75 !important; }

.metric-card {
    background: #0F1623; border: 1px solid #1E2A3A;
    border-radius: 12px; padding: 20px 24px; text-align: center;
}
.metric-value {
    font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 800;
    color: #00D4AA; line-height: 1; margin-bottom: 6px;
}
.metric-value.orange { color: #FF6B35; }
.metric-value.red { color: #EF4444; }
.metric-label {
    font-family: 'DM Mono', monospace; font-size: 10px;
    letter-spacing: 0.12em; text-transform: uppercase; color: #4B5563;
}

.stDownloadButton > button {
    background: #0F1623 !important; color: #00D4AA !important;
    border: 1px solid #00D4AA !important; border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important; font-size: 12px !important;
}
.stDownloadButton > button:hover { background: rgba(0,212,170,0.1) !important; }
</style>
""")


# ── Helpers ────────────────────────────────────────────────────────────────────
def extract_fit_score(text):
    match = re.search(r'FIT SCORE:\s*(\d+)', text, re.IGNORECASE)
    return int(match.group(1)) if match else None

def score_color_class(score):
    if score is None: return ""
    if score >= 75: return ""
    if score >= 55: return " orange"
    return " red"


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 2rem 0 1.5rem;">
    <div style="font-family:'DM Mono',monospace; font-size:11px; letter-spacing:0.15em;
                color:#00D4AA; text-transform:uppercase; margin-bottom:12px;">
        CrewAI · Claude · Tavily
    </div>
    <h1 style="font-family:'Syne',sans-serif; font-size:48px; font-weight:800;
               color:#E2E8F0; margin:0; line-height:1.1; letter-spacing:-0.03em;">
        Job Application<br>
        <span style="background:linear-gradient(135deg,#00D4AA,#0099CC);
                     -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            Intelligence System
        </span>
    </h1>
    <p style="font-family:'DM Sans',sans-serif; color:#4B5563; font-size:15px;
              margin-top:14px; max-width:520px; line-height:1.6;">
        Paste a job URL and your resume. Five AI agents research the company,
        score your fit, tailor your summary, and write your cover letter.
    </p>
    <div style="display:flex; gap:8px; align-items:center; margin-top:20px; flex-wrap:wrap;">
        <span style="background:#0F1623; border:1px solid #1E2A3A; border-radius:20px;
                     padding:5px 13px; font-family:'DM Mono',monospace; font-size:11px; color:#4B5563;">
            JD Analyzer
        </span>
        <span style="color:#1E2A3A; font-size:16px;">→</span>
        <span style="background:#0F1623; border:1px solid #1E2A3A; border-radius:20px;
                     padding:5px 13px; font-family:'DM Mono',monospace; font-size:11px; color:#4B5563;">
            Company Researcher
        </span>
        <span style="color:#1E2A3A; font-size:16px;">→</span>
        <span style="background:#0F1623; border:1px solid #1E2A3A; border-radius:20px;
                     padding:5px 13px; font-family:'DM Mono',monospace; font-size:11px; color:#4B5563;">
            Skills Gap Scorer
        </span>
        <span style="color:#1E2A3A; font-size:16px;">→</span>
        <span style="background:#0F1623; border:1px solid #1E2A3A; border-radius:20px;
                     padding:5px 13px; font-family:'DM Mono',monospace; font-size:11px; color:#4B5563;">
            Resume Tailor
        </span>
        <span style="color:#1E2A3A; font-size:16px;">→</span>
        <span style="background:#0F1623; border:1px solid #1E2A3A; border-radius:20px;
                     padding:5px 13px; font-family:'DM Mono',monospace; font-size:11px; color:#4B5563;">
            Interview Prep Writer
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Inputs ─────────────────────────────────────────────────────────────────────
job_url = st.text_input("Job URL", placeholder="https://job-boards.greenhouse.io/company/jobs/123456")
resume_text = st.text_area("Your Resume", height=220, placeholder="Paste your full resume here...")
st.write("")
run_button = st.button("Run Analysis  →", disabled=not (job_url and resume_text), use_container_width=True)


# ── Run ────────────────────────────────────────────────────────────────────────
if run_button:
    with st.spinner("Five agents running in sequence — usually 5–7 minutes..."):
        try:
            jd_analyzer = create_jd_analyzer()
            company_researcher = create_company_researcher()
            skills_gap_scorer = create_skills_gap_scorer()
            resume_tailor = create_resume_tailor()
            interview_prep_writer = create_interview_prep_writer()

            jd_task = create_jd_analysis_task(jd_analyzer, job_url)
            company_task = create_company_research_task(company_researcher, jd_task)
            skills_task = create_skills_gap_task(skills_gap_scorer, resume_text, jd_task, company_task)
            tailor_task = create_resume_tailor_task(resume_tailor, jd_task, company_task, skills_task)
            interview_task = create_interview_prep_task(
                interview_prep_writer, jd_task, company_task, skills_task, tailor_task
            )

            crew = Crew(
                agents=[jd_analyzer, company_researcher, skills_gap_scorer,
                        resume_tailor, interview_prep_writer],
                tasks=[jd_task, company_task, skills_task, tailor_task, interview_task],
                process=Process.sequential
            )

            crew.kickoff()

            st.session_state.results = {
                "jd":       jd_task.output.raw,
                "company":  company_task.output.raw,
                "skills":   skills_task.output.raw,
                "tailor":   tailor_task.output.raw,
                "interview": interview_task.output.raw
            }

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")


# ── Results ────────────────────────────────────────────────────────────────────
if "results" in st.session_state:
    st.divider()
    st.success("Analysis complete!")
    st.write("")

    # Metric cards
    fit_score = extract_fit_score(st.session_state.results["skills"])
    jd_text = st.session_state.results["jd"]
    company_match = re.search(r'COMPANY:\s*(.+)', jd_text)
    role_match = re.search(r'ROLE:\s*(.+)', jd_text)
    company_name = company_match.group(1).strip().replace("**", "").strip() if company_match else "—"
    role_name = role_match.group(1).strip().replace("**", "").strip() if role_match else "—"

    col1, col2, col3 = st.columns(3)
    with col1:
        cls = score_color_class(fit_score)
        score_display = f"{fit_score}/100" if fit_score else "—"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value{cls}">{score_display}</div>
            <div class="metric-label">Fit Score</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size:22px;padding-top:6px;">{company_name}</div>
            <div class="metric-label">Company</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        role_short = role_name[:28] + "…" if len(role_name) > 28 else role_name
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="font-size:18px;padding-top:8px;">{role_short}</div>
            <div class="metric-label">Role</div>
        </div>""", unsafe_allow_html=True)

    st.write("")

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏢  Company Intel", "📊  Skills Match", "✏️  Tailored Resume",
        "🎤  Interview Prep", "📝  Cover Letter"
    ])

    with tab1:
        st.markdown(st.session_state.results["company"])
    with tab2:
        st.markdown(st.session_state.results["skills"])
    with tab3:
        st.markdown(st.session_state.results["tailor"])
    with tab4:
        output = st.session_state.results["interview"]
        st.markdown(output.split("## COVER LETTER")[0] if "## COVER LETTER" in output else output)
    with tab5:
        output = st.session_state.results["interview"]
    if "## COVER LETTER" in output:
        cover = "## COVER LETTER" + output.split("## COVER LETTER")[1]
        st.markdown(cover)
        st.write("")

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇  Download cover letter",
                cover,
                file_name="cover_letter.txt",
                mime="text/plain"
            )
        with col2:
            if st.button("📧  Create Gmail draft"):
                try:
                    clean_text = cover.replace("## COVER LETTER", "").strip()
                    subject = f"Application: {role_name} at {company_name}"
                    create_gmail_draft(subject, clean_text)
                    st.success("Draft created — check your Gmail Drafts folder.")
                except Exception as e:
                    st.error(f"Gmail error: {str(e)}")
    else:
        st.markdown(output)