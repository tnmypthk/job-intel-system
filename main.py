from dotenv import load_dotenv
from crewai import Crew, Process
from config import DEV_JOB_URL, DEV_RESUME_FILE
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

with open(DEV_RESUME_FILE, "r") as f:
    resume_text = f.read()

jd_analyzer = create_jd_analyzer()
company_researcher = create_company_researcher()
skills_gap_scorer = create_skills_gap_scorer()
resume_tailor = create_resume_tailor()
interview_prep_writer = create_interview_prep_writer()

jd_task = create_jd_analysis_task(jd_analyzer, DEV_JOB_URL)
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
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
print("\n" + "=" * 50)
print(result)