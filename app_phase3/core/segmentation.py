import re
from typing import Dict


# Section 1: Header definitions
SECTION_HEADERS = {
    "summary": [
        "summary", "profile", "about", "professional summary"
    ],
    "experience": [
        "experience", "work experience", "employment", "professional experience"
    ],
    "education": [
        "education", "academic background", "qualifications"
    ],
    "skills": [
        "skills", "technical skills", "core competencies"
    ],
    "projects": [
        "projects", "personal projects"
    ],
    "certifications": [
        "certifications", "certificates"
    ]
}


# Section 2: Public entry point
def segment_resume(text: str) -> Dict[str, str]:
    """
    Segments resume text into logical sections using rule-based heuristics.

    Returns:
        Dict mapping section_name -> section_text
    """
    normalized_text = _normalize_text(text)
    sections = _rule_based_segmentation(normalized_text)

    # Fallback: if experience is missing or too small, assume bad formatting
    if not sections.get("experience") or len(sections["experience"]) < 200:
        return _fallback_single_block(normalized_text)

    return sections

# Section 3: Rule-based segmentation
def _rule_based_segmentation(text: str) -> Dict[str, str]:
    lines = text.split("\n")
    sections: Dict[str, str] = {}
    current_section = None

    for line in lines:
        header = _match_section_header(line)

        if header:
            current_section = header
            sections[current_section] = []
            continue

        if current_section:
            sections[current_section].append(line)

    # Join collected lines
    for key in sections:
        sections[key] = "\n".join(sections[key]).strip()

    return sections

# Section 4: Header matching logic
def _match_section_header(line: str) -> str | None:
    clean = re.sub(r"[^a-zA-Z ]", "", line).lower().strip()

    for section, headers in SECTION_HEADERS.items():
        for header in headers:
            if clean == header:
                return section

    return None

# Section 5: Text normalization
def _normalize_text(text: str) -> str:
    # Normalize bullets and whitespace
    text = text.replace("•", "-")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

# Section 6: Fallback strategy (safe default)

def _fallback_single_block(text: str) -> Dict[str, str]:
    """
    Used when resume has no clear section headers.
    Entire text is treated as experience for LLM extraction.
    """
    return {
        "summary": "",
        "experience": text,
        "education": "",
        "skills": "",
        "projects": "",
        "certifications": ""
    }
