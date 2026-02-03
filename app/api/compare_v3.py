# # app/api/compare_v3.py

# from fastapi import APIRouter
# from app.core.alignment import compute_alignment
# from app.core.prompts.alignment_prompts import ALIGNMENT_QA_PROMPT
# from app.core.llm_client import GeminiClient

# router = APIRouter()


# @router.post("/compare_v3/{job_id}/{candidate_id}/ask")
# def ask_alignment_question(
#     job_id: str,
#     candidate_id: str,
#     question: str
# ):
#     """
#     Answer alignment-related questions such as:
#     - What skills am I missing?
#     - How does my experience align with the job?
#     """

#     # 🔹 Load stored data (replace with DB later)
#     from app.store.memory import jobs, profiles

#     if job_id not in jobs:
#         # Create fallback job if missing
#         from app.core.models import JobRequirement
#         jobs[job_id] = JobRequirement(
#             job_id=job_id,
#             title="Senior Data Scientist",
#             required_skills=["python", "machine learning", "sql"],
#             preferred_skills=["tensorflow", "pytorch", "aws", "docker"],
#             min_experience_years=3,
#             description="Senior data scientist role with ML focus"
#         )

#     if candidate_id not in profiles:
#         raise ValueError(f"Candidate {candidate_id} not found")

#     job = jobs[job_id]
#     profile = profiles[candidate_id]
    
#     # Convert profile to resume format for alignment
#     resume_data = {
#         "profile": {
#             "skills": [{"name": s.name} for s in profile.skills],
#             "total_experience_years": profile.total_experience_years
#         }
#     }
    
#     # Convert job to dict format
#     job_data = {
#         "title": job.title,
#         "required_skills": job.required_skills,
#         "preferred_skills": job.preferred_skills,
#         "min_experience_years": job.min_experience_years
#     }

#     # 🔹 Step 1: Compute factual alignment
#     alignment_context = compute_alignment(
#         resume=resume_data,
#         job=job_data,
#         transferable_skills=[]  # TODO: Get from transferable store
#     )

#     # 🔹 Step 2: Ask LLM to explain
#     llm = GeminiClient()
#     prompt = ALIGNMENT_QA_PROMPT.format(
#         alignment_context=alignment_context,
#         question=question
#     )

#     answer = llm.generate(prompt)

#     return {
#         "question": question,
#         "answer": answer,
#         "alignment_context": alignment_context
#     }


# app/api/compare_v3.py

from fastapi import APIRouter, HTTPException
from app.core.alignment import compute_alignment
from app.core.prompts.alignment_prompts import ALIGNMENT_QA_PROMPT
from app.core.llm_client import GeminiClient

router = APIRouter(prefix="/compare_v3")


# -----------------------------
# Skill normalization layer
# -----------------------------

SKILL_EQUIVALENCE = {
    "logistic regression": "machine learning",
    "clustering": "machine learning",
    "predictive models": "machine learning",
    "rag": "machine learning",
    "llm": "machine learning",
    "deep learning": "machine learning",
}


def normalize_resume_skills(raw_skills):
    """
    Expands resume skills using equivalence mapping.
    """
    normalized = set()

    for skill in raw_skills:
        s = skill.lower()
        normalized.add(s)

        if s in SKILL_EQUIVALENCE:
            normalized.add(SKILL_EQUIVALENCE[s])

    return list(normalized)


# -----------------------------
# API endpoint
# -----------------------------

@router.post("/{job_id}/{candidate_id}/ask")
def ask_alignment_question(
    job_id: str,
    candidate_id: str,
    question: str
):
    """
    Answer alignment-related questions such as:
    - What skills am I missing?
    - How does my experience align with the job?
    """

    # 🔹 Load stored data (in-memory for now)
    from app.store.memory import jobs, profiles, transferable_store

    if job_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    if candidate_id not in profiles:
        raise HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found")

    job = jobs[job_id]
    profile = profiles[candidate_id]

    # -----------------------------
    # Build resume data for alignment
    # -----------------------------

    raw_resume_skills = [s.name for s in profile.skills]
    normalized_skills = normalize_resume_skills(raw_resume_skills)

    resume_data = {
        "profile": {
            "skills": [{"name": s} for s in normalized_skills],
            "total_experience_years": profile.total_experience_years
        }
    }

    job_data = {
        "title": job.title,
        "domain": job.domain,
        "required_skills": job.required_skills,
        "preferred_skills": job.preferred_skills,
        "min_experience_years": job.min_experience_years
    }

    # -----------------------------
    # Transferable skills (Phase 2 output)
    # -----------------------------

    transferable_skills = transferable_store.get(
        (candidate_id, job_id),
        []
    )

    # -----------------------------
    # Step 1: Compute alignment facts
    # -----------------------------

    alignment_context = compute_alignment(
        resume=resume_data,
        job=job_data,
        transferable_skills=transferable_skills
    )

    # -----------------------------
    # Step 2: Explain using LLM
    # -----------------------------

    llm = GeminiClient()

    prompt = ALIGNMENT_QA_PROMPT.format(
        alignment_context=alignment_context,
        question=question
    )

    answer = llm.generate(prompt)

    return {
        "question": question,
        "answer": answer,
        "alignment_context": alignment_context
    }
