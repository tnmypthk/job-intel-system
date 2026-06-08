from crewai import Agent, LLM
from config import MODEL
import os

def create_resume_tailor():
    llm = LLM(
        model=MODEL,
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    return Agent(
        role="Resume Writing Specialist",
        goal=(
            "Rewrite the candidate's professional summary and suggest targeted "
            "bullet point edits so the resume speaks directly to this specific "
            "role and company."
        ),
        backstory=(
            "You are an expert resume writer who has helped hundreds of candidates "
            "land roles at top tech companies. You never invent experience — you "
            "reframe real experience using the language and priorities of the target "
            "role. You know that hiring managers spend 7 seconds on a resume, so "
            "every word in the summary must earn its place."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )