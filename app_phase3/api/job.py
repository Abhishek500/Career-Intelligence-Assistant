from fastapi import APIRouter
from app.core.models import JobRequirement
from app.store.memory import jobs

router = APIRouter(prefix="/jobs")

@router.post("/")
def create_job(job: JobRequirement):
    jobs[job.job_id] = job
    return {"status": "stored", "job_id": job.job_id}

@router.get("/")
def list_jobs():
    return list(jobs.values())
