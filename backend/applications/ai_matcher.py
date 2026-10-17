"""
AI Skill Matching Engine.

Parses resume text (PDF, DOCX, or TXT), extracts candidate skills by keyword matching,
compares against job required skills, and returns a match percentage score (0–100).
"""

import re
import io
import urllib.request
from typing import List


# ---------------------------------------------------------------------------
# Text Extraction
# ---------------------------------------------------------------------------

def _extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract plain text from PDF bytes using PyMuPDF (fitz)."""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=file_bytes, filetype='pdf')
        text = ''
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception:
        return ''


def _extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract plain text from DOCX bytes using python-docx."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        return '\n'.join(para.text for para in doc.paragraphs)
    except Exception:
        return ''


def _extract_text_from_txt(file_bytes: bytes) -> str:
    """Decode plain text file bytes."""
    try:
        return file_bytes.decode('utf-8', errors='replace')
    except Exception:
        return ''


def _fetch_file_bytes(url: str) -> bytes:
    """Download file from a URL (http/https) or read from local path."""
    try:
        if url.startswith('http://') or url.startswith('https://'):
            with urllib.request.urlopen(url, timeout=15) as response:
                return response.read()
        else:
            # Local filesystem path
            with open(url, 'rb') as f:
                return f.read()
    except Exception:
        return b''


def extract_resume_text(cloudinary_url: str, filename: str) -> str:
    """
    Download resume from Cloudinary (or local path) and extract its text.

    Args:
        cloudinary_url: URL or local path to the uploaded resume file.
        filename: Original filename used to detect format (pdf/docx/txt).

    Returns:
        Extracted plain text string.
    """
    file_bytes = _fetch_file_bytes(cloudinary_url)
    if not file_bytes:
        return ''

    lower_name = filename.lower()
    if lower_name.endswith('.pdf'):
        return _extract_text_from_pdf(file_bytes)
    elif lower_name.endswith('.docx'):
        return _extract_text_from_docx(file_bytes)
    elif lower_name.endswith('.txt'):
        return _extract_text_from_txt(file_bytes)
    return ''


# ---------------------------------------------------------------------------
# Skill Extraction & Matching
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> List[str]:
    """Lowercase and split text into alphanumeric tokens."""
    return re.findall(r'[a-z0-9#\+\.]+', text.lower())


def _normalize_skill(skill: str) -> str:
    """Normalize a skill string for comparison."""
    return skill.strip().lower()


def calculate_match_score(resume_text: str, skills_required: str) -> float:
    """
    Compare resume text against required job skills.

    Algorithm:
    1. Split skills_required by comma into a list of required skills.
    2. Tokenize the resume text.
    3. For each required skill, check if all its sub-tokens appear in the resume tokens.
    4. Score = (matched skills / total required skills) * 100.

    Args:
        resume_text: Plain text extracted from the resume.
        skills_required: Comma-separated job skill requirements.

    Returns:
        Float match percentage in range [0.0, 100.0].
    """
    if not resume_text or not skills_required:
        return 0.0

    required_skills = [_normalize_skill(s) for s in skills_required.split(',') if s.strip()]
    if not required_skills:
        return 0.0

    resume_tokens = set(_tokenize(resume_text))

    matched = 0
    for skill in required_skills:
        skill_tokens = _tokenize(skill)
        if skill_tokens and all(token in resume_tokens for token in skill_tokens):
            matched += 1

    score = (matched / len(required_skills)) * 100.0
    return round(score, 2)


def run_skill_matching(cloudinary_url: str, original_filename: str, skills_required: str) -> dict:
    """
    Full pipeline: download resume → extract text → calculate match score.

    Returns:
        dict with keys: resume_text (str), match_score (float)
    """
    resume_text = extract_resume_text(cloudinary_url, original_filename)
    match_score = calculate_match_score(resume_text, skills_required)
    return {
        'resume_text': resume_text,
        'match_score': match_score,
    }
