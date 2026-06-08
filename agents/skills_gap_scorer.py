from crewai import Agent, LLM
from config import MODEL
import os

def create_skills_gap_scorer():
    llm = LLM(
        model=MODEL,
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    return Agent(
        role="Skills Gap Analyst",
        goal=(
            "Objectively score how well a candidate's resume matches a job "
            "description and identify specific gaps and strengths."
        ),
        backstory=(
            "You are a senior talent acquisition specialist with 10 years of "
            "experience evaluating candidates against job requirements. You are "
            "known for your honest, data-driven assessments — you do not "
            "sugarcoat gaps but you also do not overlook genuine strengths. "
            "Your fit scores are trusted because they are specific and actionable."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )