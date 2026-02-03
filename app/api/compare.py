from fastapi import APIRouter
from app.store.memory import profiles, jobs
from app.core.scoring import score_profile_against_job

router = APIRouter(prefix="/compare")

@router.post("/{job_id}/{candidate_id}")
def compare(job_id: str, candidate_id: str):
    profile = profiles[candidate_id]
    job = jobs[job_id]
    return score_profile_against_job(profile, job)
