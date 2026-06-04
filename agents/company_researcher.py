from crewai import Agent, LLM
from crewai.tools import tool
from tavily import TavilyClient
import os

@tool("Web Search")
def web_search(query: str) -> str:
    """Search the web for current information about companies, news, tech stacks, and interview processes."""
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    result = client.search(query, max_results=5)
    output = []
    for r in result.get("results", []):
        output.append(f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content']}")
    return "\n\n---\n\n".join(output)

def create_company_researcher():
    llm = LLM(
        model="claude-haiku-4-5-20251001",
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    return Agent(
        role="Company Research Specialist",
        goal=(
            "Build a comprehensive intelligence profile on the company from the "
            "job description to help a job applicant tailor their application "
            "and prepare for interviews."
        ),
        backstory=(
            "You are a meticulous researcher who specialises in uncovering what "
            "it is really like to work at a company beyond the marketing copy. "
            "You dig into news, culture, tech choices, and interview patterns "
            "to give candidates a genuine edge."
        ),
        tools=[web_search],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=8
    )