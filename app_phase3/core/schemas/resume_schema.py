# core/schemas/resume_schema.py

from pydantic import BaseModel, Field
from typing import List, Optional


# ---------- Personal ----------

class PersonalInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None


# ---------- Experience ----------

class Experience(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)
    tech_stack: List[str] = Field(default_factory=list)


# ---------- Education ----------

class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None


# ---------- Skills ----------

class Skills(BaseModel):
    programming: List[str] = Field(default_factory=list)
    ml: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)


# ---------- Resume ----------

class ResumeSchema(BaseModel):
    personal: PersonalInfo
    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    skills: Skills
