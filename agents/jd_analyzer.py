from crewai import Agent, LLM
from crewai_tools import ScrapeWebsiteTool
import os

def create_jd_analyzer():
    llm = LLM(
        model="claude-haiku-4-5-20251001",
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    return Agent(
        role="Job Description Analyst",
        goal="Extract and structure all key information from a job description URL",
        backstory=(
            "You are an expert at reading job descriptions and identifying exactly "
            "what a company is looking for. You cut through corporate language and "
            "extract the real requirements — must-haves vs nice-to-haves, technical "
            "skills vs soft skills, and the true seniority level of the role."
        ),
        tools=[ScrapeWebsiteTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )