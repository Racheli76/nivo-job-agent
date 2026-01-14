from typing import Any
from services.openai import call_openai_chat


def build_analyze_cv_prompt(text: str, lang: str = 'he') -> str:
    return (
        "You are a helpful assistant. Given the CV text, return a JSON object with keys:"
        " score (integer 0-100), summary (string), suggestions (array of short strings), bullets (array of short strings)."
        f" Respond with JSON only, in {'Hebrew' if lang=='he' else 'English'}." + "\n\nCV:\n" + text
    )


def build_match_job_prompt(cv_text: str, job_desc: str, lang: str = 'he') -> str:
    return (
        "You are a helpful assistant. Given the candidate CV and the job description, return a JSON object with keys:\n"
        "match_score (integer 0-100), common_terms (array of strings), recommended_changes (array of strings), cover_letter (string)."
        f" Respond with JSON only, in {'Hebrew' if lang=='he' else 'English'}.\n\nCV:\n" + cv_text + "\n\nJOB DESCRIPTION:\n" + job_desc
    )


def build_simulate_interview_prompt(role: str, cv_text: str = '', lang: str = 'he') -> str:
    return (
        "You are a helpful interviewer. Given the candidate CV (if available) and a role title, return a JSON object with keys:\n"
        "questions (array of 8 strings) and advice (short string)."
        f" Respond with JSON only, in {'Hebrew' if lang=='he' else 'English'}.\n\nRole:\n" + role + "\n\nCV:\n" + cv_text
    )


def run_analyze_cv(text: str, lang: str = 'he', max_tokens: int = 400) -> Any:
    prompt = build_analyze_cv_prompt(text, lang)
    return call_openai_chat([{'role': 'user', 'content': prompt}], max_tokens=max_tokens)


def run_match_job(cv_text: str, job_desc: str, lang: str = 'he', max_tokens: int = 600) -> Any:
    prompt = build_match_job_prompt(cv_text, job_desc, lang)
    return call_openai_chat([{'role': 'user', 'content': prompt}], max_tokens=max_tokens)


def run_simulate_interview(role: str, cv_text: str = '', lang: str = 'he', max_tokens: int = 800) -> Any:
    prompt = build_simulate_interview_prompt(role, cv_text, lang)
    return call_openai_chat([{'role': 'user', 'content': prompt}], max_tokens=max_tokens)
