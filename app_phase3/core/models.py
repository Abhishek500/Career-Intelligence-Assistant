from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class Skill(BaseModel):
    name: str
    category: Optional[str] = None  # e.g. "programming", "ml", "domain"
    level: Optional[str] = None     # beginner / intermediate / advanced
    years: Optional[float] = None


class Experience(BaseModel):
    title: str
    company: Optional[str]
    duration_years: Optional[float]
    skills_used: List[str] = []
    description: Optional[str]


class ProfessionalProfile(BaseModel):
    candidate_id: str
    title: Optional[str]
    total_experience_years: Optional[float]
    skills: List[Skill]
    experiences: List[Experience]


class JobRequirement(BaseModel):
    job_id: str
    title: str
    required_skills: List[str]
    preferred_skills: List[str] = []
    min_experience_years: Optional[float]
    domain: Optional[str]


class MatchBreakdown(BaseModel):
    exact_skill_matches: List[str]
    partial_skill_matches: List[str]
    missing_required_skills: List[str]
    experience_gap: Optional[float]


class MatchResult(BaseModel):
    candidate_id: str
    job_id: str
    fit_score: float
    breakdown: MatchBreakdown
