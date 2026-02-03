TRANSFERABLE_SKILL_PROMPT = """
You are evaluating transferable skills for a job fit assessment.

Candidate skills:
{candidate_skills}

Job required skills:
{job_skills}

Rules:
- Only infer transferability when defensible
- Justify using scale, data, systems, or complexity
- Do not invent experience
- Assign confidence between 0 and 1
- Output ONLY a JSON array, no markdown formatting
- Each inference must have: source_skill, target_skill, justification, confidence
- Do not include newline characters inside string values
- Keep all string values on a single line
- Do not include any additional text or comments

Example output:
[
  {{
    "source_skill": "python",
    "target_skill": "machine learning", 
    "justification": "Both require strong programming and analytical thinking",
    "confidence": 0.8
  }}
]

Now analyze and output ONLY the JSON array:
"""
