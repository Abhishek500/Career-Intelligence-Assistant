# core/prompts/resume_prompts.py

PERSONAL_PROMPT = """
You are extracting personal information from a resume.

Rules:
- Use ONLY the provided text
- Do NOT infer or guess
- If a field is missing, return null
- Output VALID JSON ONLY

Schema:
{
  "name": string | null,
  "email": string | null,
  "phone": string | null,
  "location": string | null
}
"""

EXPERIENCE_PROMPT = """
Extract work experience from the resume section below.

STRICT RULES:
- Output MUST be valid JSON
- Do NOT use ellipses ("...")
- Do NOT truncate text
- Do NOT include line breaks inside strings
- Each responsibility MUST be <= 20 words
- Rewrite responsibilities if needed to satisfy limits
- If unsure, omit the responsibility

Schema:
[
  {
    "company": string | null,
    "role": string | null,
    "start_date": string | null,
    "end_date": string | null,
    "responsibilities": [string],
    "tech_stack": [string]
  }
]
"""



EDUCATION_PROMPT = """
Extract education details from the resume section below.

Rules:
- Do NOT infer graduation year
- Use null if missing
- Output VALID JSON ONLY

Schema:
[
  {
    "degree": string | null,
    "institution": string | null,
    "year": string | null
  }
]
"""

SKILLS_PROMPT = """
Extract skills from the resume section below.

Rules:
- Categorize skills conservatively
- Do NOT invent categories
- Output VALID JSON ONLY

Schema:
{
  "programming": [string],
  "ml": [string],
  "tools": [string]
}
"""
