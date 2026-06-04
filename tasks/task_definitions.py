from crewai import Task

def create_jd_analysis_task(agent, job_url):
    return Task(
        description=f"""
        Scrape and analyze the job description at this URL: {job_url}

        Extract the following:
        1. Company name
        2. Job title and role
        3. Required skills — must-have technical skills, languages, frameworks, tools
        4. Nice-to-have skills — preferred but not required
        5. Experience level — junior/mid/senior and years if mentioned
        6. Top 5 key responsibilities
        7. Any culture signals or red flags
        """,
        expected_output="""
        A structured analysis with these exact sections:

        COMPANY: [company name]
        ROLE: [job title]
        EXPERIENCE LEVEL: [junior/mid/senior, years if mentioned]

        REQUIRED SKILLS:
        - [skill]

        NICE TO HAVE:
        - [skill]

        KEY RESPONSIBILITIES:
        - [responsibility]

        CULTURE SIGNALS:
        [2-3 sentences about work style, culture, or anything notable]
        """,
        agent=agent
    )

def create_company_research_task(agent, jd_task):
    return Task(
        description="""
        Using the company name and role from the job description analysis,
        research the company thoroughly using web search.

        Search for:
        1. Company overview — size, funding stage, industry, founding year
        2. Recent news — anything from the last 6 months
        3. Tech stack — languages, frameworks, infrastructure, data tools
        4. Work culture — values, async vs sync, how teams operate
        5. Interview process — format, difficulty, reported questions
           (search for the company name + "interview" + "glassdoor" or "reddit")

        Run multiple targeted searches. If a source is paywalled or
        inaccessible, note it and move on — do not guess or infer.
        """,
        expected_output="""
        A structured company profile with these exact sections:

        COMPANY SNAPSHOT: [3-4 sentences on size, stage, industry, founding]

        RECENT NEWS:
        - [item, with date if available]

        TECH STACK:
        - Frontend: [tools]
        - Backend: [tools]
        - Infrastructure: [tools]
        - Data / AI: [tools]

        CULTURE SIGNALS: [2-3 sentences on values, work style, team dynamics]

        INTERVIEW INTEL:
        - Format: [stages and structure]
        - Reported topics: [3-5 common themes from candidates]
        """,
        agent=agent,
        context=[jd_task]
    )

def create_skills_gap_task(agent, resume_text, jd_task, company_task):
    return Task(
        description=f"""
        You have the full job description analysis and company research from
        the previous agents. Now evaluate this candidate's resume against
        the role requirements.

        CANDIDATE RESUME:
        ---
        {resume_text}
        ---

        Compare every required skill from the JD against evidence in the resume.
        Be specific and honest. Give a realistic fit score from 0 to 100.

        For each gap, classify it as:
        - CRITICAL: a hard requirement the candidate clearly lacks
        - MODERATE: an important skill with only partial evidence
        - MINOR: a nice-to-have that is missing
        """,
        expected_output="""
        FIT SCORE: [X/100]

        MATCHED SKILLS:
        - [skill]: [specific evidence from resume]

        CRITICAL GAPS:
        - [skill]: [why it matters for this specific role]

        MODERATE GAPS:
        - [skill]: [what is missing and how to address it]

        MINOR GAPS:
        - [skill]

        STANDOUT STRENGTHS:
        - [strength]: [why this is particularly relevant to this company and role]

        OVERALL ASSESSMENT: [3-4 honest sentences]
        """,
        agent=agent,
        context=[jd_task, company_task]
    )

def create_resume_tailor_task(agent, jd_task, company_task, skills_task):
    return Task(
        description="""
        Using the job description analysis, company research, and skills gap
        assessment from the previous agents, rewrite the candidate's
        professional summary to target this specific role.

        Rules:
        - Never invent experience that does not exist in the resume
        - Use the exact language and keywords from the job description
        - Lead with the strongest match points identified in the skills gap analysis
        - Address the company's specific context (async-first, global, AI-driven)
        - The summary should be 3-5 sentences maximum

        Also identify 5 existing bullet points from the resume that should be
        reworded to better align with the JD, and provide the improved version
        of each. Focus on bullet points that address the critical or moderate
        gaps identified.
        """,
        expected_output="""
        TAILORED HEADLINE:
        [One line job title / positioning statement]

        TAILORED SUMMARY:
        [3-5 sentences rewritten to target this role and company]

        KEYWORDS TO WEAVE IN:
        [comma-separated list of exact terms from JD to include]

        BULLET POINT REWRITES:
        Original: [exact original text]
        Improved: [rewritten version using JD language]

        Original: [exact original text]
        Improved: [rewritten version]

        [repeat for 5 bullet points]

        WHAT NOT TO CHANGE: [2-3 sentences on what is already well-positioned]
        """,
        agent=agent,
        context=[jd_task, company_task, skills_task]
    )

def create_interview_prep_task(agent, jd_task, company_task, skills_task, tailor_task):
    return Task(
        description="""
        Using all previous analysis — the JD breakdown, company research,
        skills gap assessment, and tailored resume — produce two things:

        1. Ten interview questions this candidate is likely to face for
           this specific role at this specific company. For each question:
           - Write the question as the interviewer would ask it
           - Explain what the interviewer is really testing
           - Give a 2-3 sentence answer framework using the candidate's
             actual experience

        2. A cover letter draft that:
           - Opens with something specific about Remote (not generic praise)
           - Addresses the "bridge builder" positioning angle
           - Acknowledges the CX domain transition directly and briefly
           - Is no longer than 4 paragraphs
           - Sounds like a human wrote it, not a template
        """,
        expected_output="""
        INTERVIEW QUESTIONS:

        Q1: [question]
        What they're testing: [1 sentence]
        Answer framework: [2-3 sentences using candidate's real experience]

        Q2: [question]
        What they're testing: [1 sentence]
        Answer framework: [2-3 sentences]

        [continue through Q10]

        ---

        COVER LETTER:

        [4 paragraphs, ready to use with minor personalisation]
        """,
        agent=agent,
        context=[jd_task, company_task, skills_task, tailor_task]
    )