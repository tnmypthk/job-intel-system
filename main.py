# main.py — CLI test runner (use app.py for the Streamlit UI)
from dotenv import load_dotenv
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

# Replace job_url and resume.txt with your own inputs to test agents individually
job_url = "https://job-boards.greenhouse.io/remotecom/jobs/7747671003"

with open("resume.txt", "r") as f:
    resume_text = f.read()

# Agents
jd_analyzer = create_jd_analyzer()
company_researcher = create_company_researcher()
skills_gap_scorer = create_skills_gap_scorer()
resume_tailor = create_resume_tailor()
interview_prep_writer = create_interview_prep_writer()

# Tasks
jd_task = create_jd_analysis_task(jd_analyzer, job_url)
company_task = create_company_research_task(company_researcher, jd_task)
skills_task = create_skills_gap_task(skills_gap_scorer, resume_text, jd_task, company_task)
tailor_task = create_resume_tailor_task(resume_tailor, jd_task, company_task, skills_task)
interview_task = create_interview_prep_task(
    interview_prep_writer, jd_task, company_task, skills_task, tailor_task
)

# Crew
crew = Crew(
    agents=[jd_analyzer, company_researcher, skills_gap_scorer,
            resume_tailor, interview_prep_writer],
    tasks=[jd_task, company_task, skills_task, tailor_task, interview_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()

print("\n" + "=" * 50)
print("INTERVIEW PREP + COVER LETTER:")
print("=" * 50)
print(result)