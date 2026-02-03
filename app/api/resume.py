# from fastapi import APIRouter
# from app.core.models import ProfessionalProfile
# from app.store.memory import profiles

# router = APIRouter(prefix="/resume")

# @router.post("/")
# def upload_resume(profile: ProfessionalProfile):
#     profiles[profile.candidate_id] = profile
#     return {"status": "stored", "candidate_id": profile.candidate_id}



# api/resume.py

from fastapi import APIRouter, UploadFile, File
import tempfile
import shutil
import uuid

from app.pipelines.resume_pipeline import ResumeExtractionPipeline
from app.core.llm_client import GeminiClient
from app.core.models import ProfessionalProfile, Skill, Experience
from app.store.memory import profiles

router = APIRouter()


@router.post("/resume/extract")
def extract_resume(file: UploadFile = File(...)):
    """
    Upload a resume (PDF/DOCX) and return structured resume JSON.
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    llm = GeminiClient()
    pipeline = ResumeExtractionPipeline(llm)

    # Extract structured data
    result = pipeline.run(tmp_path)
    
    # Convert to ProfessionalProfile format
    candidate_id = f"candidate_{uuid.uuid4().hex[:8]}"
    
    # Convert skills
    skills = []
    for skill_name in result.skills.programming + result.skills.ml + result.skills.tools:
        skills.append(Skill(name=skill_name, level="intermediate"))  # Default level
    
    # Convert experience
    experiences = []
    for exp in result.experience:
        # Calculate duration years from start/end dates
        duration_years = None
        try:
            if exp.start_date and exp.end_date:
                # Simple year calculation - could be improved
                start_year = int(exp.start_date.split('/')[-1]) if '/' in exp.start_date else 0
                if exp.end_date.lower() == 'current':
                    import datetime
                    end_year = datetime.datetime.now().year
                else:
                    end_year = int(exp.end_date.split('/')[-1]) if '/' in exp.end_date else 0
                duration_years = max(0, end_year - start_year)
        except:
            pass
        
        experiences.append(Experience(
            title=exp.role or "Unknown Role",
            company=exp.company or "Unknown Company",
            duration_years=duration_years,
            skills_used=exp.tech_stack or [],
            description="; ".join(exp.responsibilities[:3]) if exp.responsibilities else ""
        ))
    
    # Create profile
    profile = ProfessionalProfile(
        candidate_id=candidate_id,
        name=result.personal.name or "Unknown Name",
        email=result.personal.email or "",
        phone=result.personal.phone or "",
        title=result.experience[0].role if result.experience and result.experience[0].role else "Professional",
        total_experience_years=len(result.experience),  # Simple count as placeholder
        skills=skills,
        experiences=experiences,
        summary=result.personal.location or ""  # Using location as summary for now
    )
    
    # Store in memory
    profiles[candidate_id] = profile
    
    return {
        "candidate_id": candidate_id,
        "profile": profile.dict(),
        "extracted_data": result.dict()
    }
