from pydantic import BaseModel, Field
from typing import List, Optional


# -----------------------------
# Skill & Domain Reasoning
# -----------------------------

class TransferableSkillInference(BaseModel):
    source_skill: str
    target_skill: str
    justification: str
    confidence: float = Field(ge=0.0, le=1.0)


class DomainSignal(BaseModel):
    signal: str
    explanation: str


# -----------------------------
# Experience Reasoning
# -----------------------------

class ExperienceAlignment(BaseModel):
    years_required: float
    years_actual: float
    meets_requirement: bool


# -----------------------------
# Full Reasoning Trace
# -----------------------------

class ReasoningTrace(BaseModel):
    exact_matches: List[str]
    transferable_inferences: List[TransferableSkillInference]
    domain_signals: List[DomainSignal]
    experience_alignment: ExperienceAlignment
    gaps: List[str]


# -----------------------------
# Match Summary (Scoring + Reasoning)
# -----------------------------

class MatchSummary(BaseModel):
    candidate_id: str
    job_id: str
    fit_score: float
    reasoning: ReasoningTrace


# -----------------------------
# Question Answering Output
# -----------------------------

class AlignmentAnswer(BaseModel):
    question: str
    answer: str
    reasoning_used: Optional[ReasoningTrace] = None


# -----------------------------
# Reasoning Entry Point
# -----------------------------

def answer_question(question: str, alignment_context: dict, llm):
    """
    Uses LLM to explain alignment facts.
    LLM must NOT compute new facts.
    """

    from app.core.prompts.alignment_prompts import ALIGNMENT_QA_PROMPT

    prompt = ALIGNMENT_QA_PROMPT.format(
        alignment_context=alignment_context,
        question=question
    )

    answer = llm.complete(prompt)

    return AlignmentAnswer(
        question=question,
        answer=answer
    )
