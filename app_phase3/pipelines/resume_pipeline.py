from app.core.ingestion import extract_text
from app.core.segmentation import segment_resume
from app.core.extraction import extract_resume_structured
from app.core.normalize import normalize_resume
from app.core.schemas.resume_schema import ResumeSchema

class ResumeExtractionPipeline:
    def __init__(self, llm_client):
        self.llm = llm_client

    def run(self, file_path: str) -> ResumeSchema:
        raw_text = extract_text(file_path)
        sections = segment_resume(raw_text)
        extracted = extract_resume_structured(sections, self.llm)
        normalized = normalize_resume(extracted)
        return ResumeSchema.model_validate(normalized)
