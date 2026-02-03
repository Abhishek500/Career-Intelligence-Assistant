from typing import Dict, Tuple, List
from app.core.models import ProfessionalProfile, JobRequirement
from app.core.reasoning_models import TransferableSkillInference

profiles: Dict[str, ProfessionalProfile] = {}
jobs: Dict[str, JobRequirement] = {}
transferable_store: Dict[Tuple[str, str], List[TransferableSkillInference]] = {}
