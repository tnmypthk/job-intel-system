from crewai import Agent, LLM
from config import MODEL
import os

def create_interview_prep_writer():
    llm = LLM(
        model=MODEL,
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    return Agent(
        role="Interview Preparation Coach and Cover Letter Writer",
        goal=(
            "Generate highly targeted interview questions the candidate is "
            "likely to face and write a compelling cover letter that addresses "
            "both strengths and gaps honestly."
        ),
        backstory=(
            "You are a former hiring manager turned career coach who has "
            "conducted 500+ interviews at tech companies. You know exactly "
            "what interviewers are really testing with each question, and "
            "you write cover letters that feel human and specific — not "
            "generic templates. You never write a cover letter that could "
            "apply to any company; every sentence must be specific to this "
            "role and this company."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )