# Job Application Intelligence System

A multi-agent AI system that automates job application research and preparation.
Paste a job URL and your resume — five AI agents research the company, score your
fit, identify skill gaps, tailor your professional summary, generate interview
questions, and write a cover letter.

---

## Agent Architecture

Five CrewAI agents run in sequence, each building on the previous agent's output:
JD Analyzer → Company Researcher → Skills Gap Scorer → Resume Tailor → Interview Prep Writer

| Agent | What it does | Tools |
|---|---|---|
| JD Analyzer | Scrapes and parses the job description | ScrapeWebsiteTool |
| Company Researcher | Researches company news, culture, tech stack, interview intel | Tavily web search |
| Skills Gap Scorer | Scores resume fit 0–100, flags critical/moderate/minor gaps | LLM reasoning |
| Resume Tailor | Rewrites professional summary using JD language | LLM reasoning |
| Interview Prep Writer | Generates 10 targeted questions + cover letter draft | LLM reasoning |

---

## Tech Stack

- **Agent framework**: CrewAI
- **LLM**: Anthropic Claude (claude-haiku-4-5)
- **Web search**: Tavily
- **UI**: Streamlit
- **Language**: Python 3.11

---

## Setup

### Prerequisites

- Python 3.11+
- [Anthropic API key](https://console.anthropic.com)
- [Tavily API key](https://tavily.com)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/job-intel-system.git
cd job-intel-system

# 2. Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Open .env and add your API keys
```

### Run

```bash
streamlit run app.py
```

---

## Usage

1. Paste a public job posting URL (Greenhouse, Lever, or similar)
2. Paste your resume as plain text
3. Click **Run Analysis** — takes 5–7 minutes
4. Review results across five tabs

---

## Output Tabs

| Tab | Content |
|---|---|
| Company Intel | Overview, recent news, tech stack, culture signals, interview intel |
| Skills Match | Fit score (0–100), matched skills, critical/moderate/minor gaps |
| Tailored Resume | Rewritten summary + 5 bullet point rewrites using JD language |
| Interview Prep | 10 likely questions with answer frameworks using your real experience |
| Cover Letter | Ready-to-use cover letter draft + download button |

---

## Project Structure
job-intel-system/
    ├── agents/
    │   ├── jd_analyzer.py
    │   ├── company_researcher.py
    │   ├── skills_gap_scorer.py
    │   ├── resume_tailor.py
    │   └── interview_prep_writer.py
    ├── tasks/
    │   └── task_definitions.py
    ├── tools/
    │   └── search_tools.py
    ├── app.py               # Streamlit UI
    ├── main.py              # CLI runner for testing individual agents
    ├── requirements.txt
    ├── .env.example
    └── README.md

---

## Roadmap

- [x] Five-agent CrewAI pipeline
- [x] Streamlit dashboard with metric cards and styled tabs
- [ ] Google Drive MCP — read resume from Drive instead of pasting
- [ ] Gmail MCP — auto-create cover letter as Gmail draft
- [ ] Upgrade to claude-sonnet-4-6 for production-quality output
- [ ] PDF resume upload support
- [ ] Save and compare multiple job analyses

---

## Built With

Built as a hands-on project to demonstrate multi-agent AI systems, LLM integration,
web search automation, and MCP integration (coming soon).

---

## Notes

- Avoid LinkedIn job URLs — they block scrapers. Use Greenhouse or Lever URLs.
- `resume.txt` is gitignored — never commit your resume to a public repo.
- `main.py` is a CLI test runner. The production entry point is `app.py`.