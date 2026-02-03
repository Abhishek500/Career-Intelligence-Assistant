# core/ingestion.py

from pathlib import Path
from typing import Union
import pdfplumber
from docx import Document


def extract_text(file_path: Union[str, Path]) -> str:
    """
    Extract raw text from a resume file.
    Supported formats: PDF, DOCX

    Returns:
        Plain text with line breaks preserved
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return _extract_pdf_text(file_path)
    elif suffix == ".docx":
        return _extract_docx_text(file_path)
    else:
        raise ValueError(f"Unsupported resume format: {suffix}")


def _extract_pdf_text(file_path: Path) -> str:
    text_chunks = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)

    if not text_chunks:
        raise ValueError("No text could be extracted from PDF")

    return "\n".join(text_chunks)


def _extract_docx_text(file_path: Path) -> str:
    doc = Document(file_path)

    text_chunks = [
        para.text.strip()
        for para in doc.paragraphs
        if para.text and para.text.strip()
    ]

    if not text_chunks:
        raise ValueError("No text could be extracted from DOCX")

    return "\n".join(text_chunks)
