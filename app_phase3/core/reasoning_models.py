from pydantic import BaseModel, Field
from typing import List


class TransferableSkillInference(BaseModel):
    source_skill: str
    target_skill: str
    justification: str
    confidence: float = Field(ge=0.0, le=1.0)


class DomainSignal(BaseModel):
    signal: str
    explanation: str


class ReasoningTrace(BaseModel):
    exact_matches: List[str]
    transferable_inferences: List[TransferableSkillInference]
    domain_signals: List[DomainSignal]
    gaps: List[str]


class Phase2MatchResult(BaseModel):
    candidate_id: str
    job_id: str
    fit_score: float
    reasoning: ReasoningTrace
