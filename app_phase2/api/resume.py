from fastapi import APIRouter
from app.core.models import ProfessionalProfile
from app.store.memory import profiles

router = APIRouter(prefix="/resume")

@router.post("/")
def upload_resume(profile: ProfessionalProfile):
    profiles[profile.candidate_id] = profile
    return {"status": "stored", "candidate_id": profile.candidate_id}
