import re
from typing import List
from .models import Skill, Experience


COMMON_SKILLS = {
    "python", "sql", "machine learning", "deep learning",
    "pytorch", "tensorflow", "nlp", "statistics",
    "fastapi", "docker", "aws", "snowflake"
}


def extract_skills(text: str) -> List[Skill]:
    text_lower = text.lower()
    found = []

    for skill in COMMON_SKILLS:
        if skill in text_lower:
            found.append(Skill(name=skill))

    return found


def estimate_experience_years(text: str) -> float | None:
    match = re.search(r"(\d+)\+?\s+years", text.lower())
    if match:
        return float(match.group(1))
    return None
