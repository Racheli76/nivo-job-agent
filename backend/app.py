from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from config import settings
from typing import Any, Dict, Optional
import json
import uuid
import time
import zipfile
import io
import re

# rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse


# When MOCK_MODE is true the server will return deterministic mock data
MOCK_MODE = settings.mock_mode
OPENAI_API_KEY = settings.openai_api_key

app = FastAPI(title="Job Agent API")

# Rate limiter (uses client IP by default)
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit_default])
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Global handler for rate limit exceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(status_code=429, content={"error": "rate_limit_exceeded"})

# Allow the frontend (vite default) and local testing to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CVText(BaseModel):
    text: Optional[str] = None
    session_id: Optional[str] = None
    job_desc: Optional[str] = None  # Optional job description for CV tailoring

class JobDesc(BaseModel):
    title: str = ""
    description: str
    session_id: Optional[str] = None


class TranslatePayload(BaseModel):
    text: str
    target: str = "en"

class DecidePayload(BaseModel):
    session_id: str

# Session store (may be Redis or in-memory)
from session_store import session_store


def _parse_json_from_text(text: str) -> Any:
    """Try to extract a JSON object from a model response text.
    Returns Python object or raises ValueError.
    """
    # try direct load
    try:
        return json.loads(text)
    except Exception:
        pass

    # find first { and last }
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        snippet = text[start:end+1]
        try:
            return json.loads(snippet)
        except Exception:
            pass

    # no JSON found
    raise ValueError('No JSON object found')


def _detect_language(text: str) -> str:
    """Naive detection: returns 'he' if Hebrew characters found, else 'en'"""
    if not text:
        return 'en'
    try:
        if re.search(r"[\u0590-\u05FF]", text):
            return 'he'
    except Exception:
        pass
    return 'en'

# --- mocks ---

from mocks import mock_analyze_cv, mock_match_job, mock_simulate_interview
from services.openai import openai_available as _openai_available, call_openai_chat as _call_openai_chat


def _extract_text_from_docx_bytes(data: bytes) -> str:
    """Lightweight docx extractor without extra dependencies.
    Reads word/document.xml from the .docx zip and strips tags.
    """
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
        name = 'word/document.xml'
        if name not in z.namelist():
            return ''
        xml = z.read(name).decode('utf-8', errors='ignore')
        # strip tags naively
        text = re.sub(r'<[^>]+>', ' ', xml)
        # collapse whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except Exception:
        return ''

# --- endpoints ---
@app.post('/analyze-cv')
async def analyze_cv(body: CVText):
    # prefer session-stored CV if session_id provided
    text = ''
    session_lang = None
    if body.session_id:
        s = await session_store.get(body.session_id)
        if s:
            text = s.get('cv_text', '')
            session_lang = s.get('lang')
    if not text:
        text = body.text or ''
    lang = session_lang or _detect_language(text)
    job_desc = body.job_desc or ''
    if MOCK_MODE:
        return {"result": mock_analyze_cv(text, lang, job_desc)}
    if not _openai_available():
        return {"error": "OpenAI API key not configured. Set OPENAI_API_KEY or enable MOCK_MODE."}
    try:
        from services.prompting import run_analyze_cv
        content = run_analyze_cv(text, job_desc, lang, max_tokens=2000)
        try:
            parsed = _parse_json_from_text(content)
            return {"result": parsed}
        except Exception:
            return {"result": content}
    except Exception as e:
        return {"error": str(e)}

@app.post('/match-job')
async def match_job(data: JobDesc):
    # find CV from session if provided
    cv_text = ''
    session_lang = None
    if data.session_id:
        s = await session_store.get(data.session_id)
        if s:
            cv_text = s.get('cv_text', '')
            session_lang = s.get('lang')
        # store job text/title in session for later decide
        s = s or {}
        s.update({'job_desc': data.description, 'job_title': data.title})
        await session_store.set(data.session_id, s)
    if not cv_text:
        cv_text = ''
    lang = session_lang or _detect_language(cv_text or data.description or '')
    if MOCK_MODE:
        return {"result": mock_match_job(cv_text, data.description, lang)}
    if not _openai_available():
        return {"error": "OpenAI API key not configured. Set OPENAI_API_KEY or enable MOCK_MODE."}
    try:
        from services.prompting import run_match_job
        content = run_match_job(cv_text, data.description, lang, max_tokens=600)
        try:
            parsed = _parse_json_from_text(content)
            return {"result": parsed}
        except Exception:
            return {"result": content}
    except Exception as e:
        return {"error": str(e)}

@app.post('/simulate-interview')
async def simulate_interview(title: str = Form(...)):
    # Accept a combined title possibly containing session id separated by '||' (frontend uses this)
    role = title
    session_id = None
    if '||' in title:
        parts = title.split('||', 1)
        role = parts[0]
        session_id = parts[1]

    cv_text = ''
    session_lang = None
    if session_id:
        s = await session_store.get(session_id)
        if s:
            cv_text = s.get('cv_text', '')
            session_lang = s.get('lang')

    lang = session_lang or _detect_language(cv_text)

    if MOCK_MODE:
        return {"result": mock_simulate_interview(role, lang)}
    if not _openai_available():
        return {"error": "OpenAI API key not configured. Set OPENAI_API_KEY or enable MOCK_MODE."}
    try:
        from services.prompting import run_simulate_interview
        content = run_simulate_interview(role, cv_text, lang, max_tokens=800)
        content = run_simulate_interview(role, cv_text, lang, max_tokens=800)
        try:
            parsed = _parse_json_from_text(content)
            return {"result": parsed}
        except Exception:
            return {"result": content}
    except Exception as e:
        return {"error": str(e)}

@app.post('/upload-cv-file')
async def upload_cv_file(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename or 'file'
    text = ''

    # reject huge files early
    if len(contents) > settings.max_upload_size_bytes:
        return {"error": "file_too_large", "max_size": settings.max_upload_size_bytes}

    # handle .docx without extra deps
    if filename.lower().endswith('.docx'):
        text = _extract_text_from_docx_bytes(contents)
        if not text:
            text = '[Could not extract text from docx]'
    else:
        try:
            text = contents.decode('utf-8')
        except Exception:
            # binary fallback: return a short hexdump-like preview
            text = f'[binary file: {len(contents)} bytes]'

    # detect language and create session to store CV text for subsequent calls
    lang = _detect_language(text)
    session_id = str(uuid.uuid4())
    await session_store.set(session_id, {"cv_text": text, "uploaded_at": time.time(), "filename": filename, "lang": lang})

    return {"filename": filename, "text_preview": text[:20000], "length": len(contents), "session_id": session_id, "lang": lang}


@app.post('/translate')
async def translate(payload: TranslatePayload):
    text = payload.text
    target = payload.target
    if MOCK_MODE:
        # naive mock: return original text with note
        return {"translation": text + f" (mock-> {target})"}
    if not _openai_available():
        return {"error": "OpenAI API key not configured. Set OPENAI_API_KEY or enable MOCK_MODE."}
    try:
        prompt = f"Translate the following text to {target}. Return only the translation:\n\n{text}"
        content = _call_openai_chat([{'role': 'user', 'content': prompt}], max_tokens=500)
        return {"translation": content}
    except Exception as e:
        return {"error": str(e)}


@app.post('/decide')
async def decide(payload: DecidePayload):
    session_id = payload.session_id
    s = await session_store.get(session_id)
    if not s:
        return {"error": "session_not_found"}
    cv_text = s.get('cv_text', '').strip()
    job_desc = s.get('job_desc', '').strip()
    if not cv_text or not job_desc:
        missing = []
        if not cv_text: missing.append('cv')
        if not job_desc: missing.append('job')
        return {"error":"missing_inputs", "missing": missing}
    try:
        # reuse match_job logic to compute a match score
        match_resp = await match_job(JobDesc(title=s.get('job_title',''), description=job_desc, session_id=session_id))
        if isinstance(match_resp, dict) and match_resp.get('error'):
            return {"error":"match_error", "detail": match_resp.get('error')}
        match_result = match_resp.get('result') if isinstance(match_resp, dict) else None
        match_score = None
        if isinstance(match_result, dict):
            match_score = match_result.get('match_score')
        if match_score is None and isinstance(match_result, str):
            try:
                parsed = _parse_json_from_text(match_result)
                match_score = parsed.get('match_score')
            except Exception:
                match_score = None
        threshold = settings.decide_threshold
        action = 'prep_interview' if (isinstance(match_score, int) and match_score >= threshold) else 'improve_cv'
        return {"action": action, "match_score": match_score, "reason": f"threshold_{threshold}"}
    except Exception as e:
        return {"error": "decision_error", "detail": str(e)}


@app.get('/health')
async def health():
    return {"status": "ok", "mock_mode": MOCK_MODE}

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
