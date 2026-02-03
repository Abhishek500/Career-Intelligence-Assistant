from typing import Dict
import json
from app.core.prompts.resume_prompts import (
    PERSONAL_PROMPT,
    EXPERIENCE_PROMPT,
    EDUCATION_PROMPT,
    SKILLS_PROMPT,
)


def extract_resume_structured(
    sections: Dict[str, str],
    llm_client
) -> Dict:
    """
    Extract structured resume data from segmented sections using LLM.

    Returns raw (unvalidated) JSON-compatible dict.
    """

    extracted = {}

    # Personal info is often spread across entire resume
    personal_raw = llm_client.extract(
        prompt=PERSONAL_PROMPT,
        input_text=_merge_sections(sections)
    )
    extracted["personal"] = _parse_json_response(personal_raw, {})

    experience_raw = llm_client.extract(
        prompt=EXPERIENCE_PROMPT,
        input_text=sections.get("experience", "")
    )
    extracted["experience"] = _parse_json_response(experience_raw, [])

    education_raw = llm_client.extract(
        prompt=EDUCATION_PROMPT,
        input_text=sections.get("education", "")
    )
    extracted["education"] = _parse_json_response(education_raw, [])

    skills_raw = llm_client.extract(
        prompt=SKILLS_PROMPT,
        input_text=sections.get("skills", "")
    )
    extracted["skills"] = _parse_json_response(skills_raw, {})

    return extracted


def _parse_json_response(response: str, default):
    """Parse JSON response from LLM, with fallback to default."""
    try:
        # Clean response - remove markdown code blocks if present
        cleaned = response.strip()
        if cleaned.startswith('```json'):
            cleaned = cleaned[7:]  # Remove ```json
        if cleaned.startswith('```'):
            cleaned = cleaned[3:]   # Remove ```
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]  # Remove trailing ```
        cleaned = cleaned.strip()
        
        # Try to parse JSON
        return json.loads(cleaned)
    except Exception as e:
        print(f"⚠️ Failed to parse JSON response: {e}")
        print(f"   Raw response: {response[:200]}...")
        
        # Try to repair incomplete JSON
        try:
            return _repair_json(cleaned, default)
        except:
            return default


def _repair_json(json_str: str, default):
    """Attempt to repair incomplete JSON."""
    print(f"🔧 Raw truncated response: {json_str[:200]}...")
    
    # If it's clearly truncated, return default
    if '...' in json_str or json_str.rstrip().endswith('[') or json_str.rstrip().endswith('{'):
        print("🔧 Response appears truncated, using default")
        return default
    
    # Fix incomplete strings - look for unclosed quotes
    lines = json_str.split('\n')
    repaired_lines = []
    for line_num, line in enumerate(lines):
        # Skip lines that are clearly truncated
        if '...' in line or line.rstrip().endswith('...'):
            print(f"🔧 Skipping truncated line {line_num}: {line[:50]}...")
            continue
            
        # Count quotes to detect unclosed strings
        quote_count = line.count('"')
        if quote_count % 2 != 0:  # Odd number = unclosed quote
            # Find the last quote and close the string properly
            last_quote_pos = line.rfind('"')
            if last_quote_pos != -1:
                # Close the string and remove any trailing comma
                before_quote = line[:last_quote_pos + 1]
                after_quote = line[last_quote_pos + 1:].rstrip().rstrip(',')
                line = before_quote + after_quote
                print(f"🔧 Fixed unclosed quote in line {line_num}")
        
        # Remove trailing commas from incomplete lines
        if line.strip().endswith(','):
            line = line.rstrip(',')
            
        repaired_lines.append(line)
    
    repaired = '\n'.join(repaired_lines)
    
    # Ensure array/object is closed properly
    open_brackets = repaired.count('[') - repaired.count(']')
    open_braces = repaired.count('{') - repaired.count('}')
    
    if open_brackets > 0:
        repaired += ']' * open_brackets
        print(f"🔧 Added {open_brackets} closing brackets")
    if open_braces > 0:
        repaired += '}' * open_braces
        print(f"🔧 Added {open_braces} closing braces")
    
    try:
        result = json.loads(repaired)
        print(f"✅ Successfully repaired JSON")
        return result
    except Exception as e:
        print(f"🔧 JSON repair failed: {e}")
        print(f"🔧 Final repaired string: {repaired[:200]}...")
        return default


def _merge_sections(sections: Dict[str, str]) -> str:
    """
    Used for personal info extraction where data may appear anywhere.
    """
    return "\n\n".join(
        value for value in sections.values() if value
    )
