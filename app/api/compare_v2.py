from fastapi import APIRouter
from app.store.memory import profiles, jobs
from app.core.evaluator import Phase2Evaluator

router = APIRouter(prefix="/compare_v2")

evaluator = Phase2Evaluator()


@router.post("/{job_id}/{candidate_id}")
def compare_v2(job_id: str, candidate_id: str):
    return evaluator.evaluate(
        profiles[candidate_id],
        jobs[job_id]
    )
