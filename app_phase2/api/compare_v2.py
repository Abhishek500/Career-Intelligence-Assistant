from fastapi import APIRouter
from app.store.memory import profiles, jobs
from app.core.evaluator import Phase2Evaluator
from app.core.models import JobRequirement

router = APIRouter(prefix="/compare_v2")

evaluator = Phase2Evaluator()


@router.post("/{job_id}/{candidate_id}")
def compare_v2(job_id: str, candidate_id: str):
    print(f"🔍 Looking for job_id: {job_id}")
    print(f"🔍 Available jobs: {list(jobs.keys())}")
    
    if job_id not in jobs:
        print(f"⚠️ Job {job_id} not found, creating fallback job")
        # Create a fallback senior data scientist job
        jobs[job_id] = JobRequirement(
            job_id=job_id,
            title="Senior Data Scientist",
            required_skills=["python", "machine learning", "sql"],
            preferred_skills=["tensorflow", "pytorch", "aws", "docker"],
            min_experience_years=3,
            description="Senior data scientist role with ML focus"
        )
        print(f"✅ Created fallback job: {job_id}")
    
    if candidate_id not in profiles:
        raise ValueError(f"Candidate {candidate_id} not found")
    
    return evaluator.evaluate(
        profiles[candidate_id],
        jobs[job_id]
    )
