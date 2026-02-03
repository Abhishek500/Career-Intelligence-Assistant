from .models import ProfessionalProfile, JobRequirement, MatchResult, MatchBreakdown


def score_profile_against_job(
    profile: ProfessionalProfile,
    job: JobRequirement
) -> MatchResult:

    profile_skills = {s.name.lower() for s in profile.skills}
    required = {s.lower() for s in job.required_skills}
    preferred = {s.lower() for s in job.preferred_skills}

    exact_matches = list(profile_skills & required)
    missing = list(required - profile_skills)
    partial = list(profile_skills & preferred)

    skill_score = (
        len(exact_matches) * 1.0 +
        len(partial) * 0.5
    )

    max_skill_score = len(required) * 1.0 + len(preferred) * 0.5
    normalized_skill_score = skill_score / max(max_skill_score, 1)

    exp_gap = None
    if job.min_experience_years and profile.total_experience_years:
        exp_gap = profile.total_experience_years - job.min_experience_years

    fit_score = round(normalized_skill_score * 100, 2)

    return MatchResult(
        candidate_id=profile.candidate_id,
        job_id=job.job_id,
        fit_score=fit_score,
        breakdown=MatchBreakdown(
            exact_skill_matches=exact_matches,
            partial_skill_matches=partial,
            missing_required_skills=missing,
            experience_gap=exp_gap
        )
    )
