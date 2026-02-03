from typing import Dict, List


def compute_alignment(
    resume: Dict,
    job: Dict,
    transferable_skills: List[Dict]
) -> Dict:
    """
    Computes factual alignment between a resume and a job.
    No LLM usage. Deterministic only.
    """

    resume_skills = {
        s["name"].lower()
        for s in resume["profile"]["skills"]
    }

    required_skills = {s.lower() for s in job["required_skills"]}
    preferred_skills = {s.lower() for s in job.get("preferred_skills", [])}

    # Add transferable skills to resume skills for matching
    transferable_targets = {
        inf.target_skill.lower()
        for inf in transferable_skills
        if inf.target_skill
    }
    
    # Combine direct skills + transferable targets
    all_candidate_skills = resume_skills | transferable_targets

    matched_required = sorted(all_candidate_skills & required_skills)
    missing_required = sorted(required_skills - all_candidate_skills)

    matched_preferred = sorted(all_candidate_skills & preferred_skills)
    missing_preferred = sorted(preferred_skills - all_candidate_skills)

    years_actual = resume["profile"].get("total_experience_years", 0)
    years_required = job.get("min_experience_years", 0)

    experience_alignment = {
        "years_required": years_required,
        "years_actual": years_actual,
        "meets_requirement": years_actual >= years_required
    }

    return {
        "matched_required_skills": matched_required,
        "missing_required_skills": missing_required,
        "matched_preferred_skills": matched_preferred,
        "missing_preferred_skills": missing_preferred,
        "transferable_skills": transferable_skills,
        "experience_alignment": experience_alignment,
        "job_context": {
            "title": job["title"],
            "domain": job.get("domain")
        }
    }
