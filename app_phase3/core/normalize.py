# SKILL_ALIASES = {
#     "ml": "machine learning",
#     "dl": "deep learning",
#     "tf": "tensorflow"
# }


# def normalize_skill_name(name: str) -> str:
#     name = name.lower().strip()
#     return SKILL_ALIASES.get(name, name)




import re
from typing import Dict


def normalize_resume(resume: Dict) -> Dict:
    print(f"🔍 Debug: Resume data type: {type(resume)}")
    print(f"🔍 Debug: Experience data type: {type(resume.get('experience', []))}")
    print(f"🔍 Debug: Experience data: {resume.get('experience', [])}")
    
    # Handle case where LLM returns string instead of list
    experience_data = resume.get("experience", [])
    if isinstance(experience_data, str):
        print("⚠️ Experience is string, attempting to parse as JSON")
        try:
            import json
            experience_data = json.loads(experience_data)
        except:
            print("❌ Failed to parse experience as JSON, using empty list")
            experience_data = []
    
    resume["experience"] = [
        _normalize_experience(e) for e in experience_data
    ]

    resume["skills"] = _normalize_skills(resume.get("skills", {}))

    return resume


def _normalize_experience(exp: Dict) -> Dict:
    exp["start_date"] = _normalize_date(exp.get("start_date"))
    exp["end_date"] = _normalize_date(exp.get("end_date"))

    exp["tech_stack"] = _dedupe_list(exp.get("tech_stack", []))
    exp["responsibilities"] = _clean_list(exp.get("responsibilities", []))

    return exp


def _normalize_skills(skills: Dict) -> Dict:
    return {
        k: _dedupe_list(v)
        for k, v in skills.items()
    }


def _normalize_date(date_str: str | None) -> str | None:
    if not date_str:
        return None

    date_str = date_str.strip()

    # Handle "Present"
    if date_str.lower() in {"present", "current"}:
        return "Present"

    # Normalize formats like "Sept 2021" → "2021-09"
    match = re.search(r"(19|20)\d{2}", date_str)
    if match:
        return match.group(0)

    return date_str


def _dedupe_list(items):
    seen = set()
    result = []
    for item in items:
        clean = item.strip()
        if clean and clean.lower() not in seen:
            seen.add(clean.lower())
            result.append(clean)
    return result


def _clean_list(items):
    return [i.strip() for i in items if i and i.strip()]
