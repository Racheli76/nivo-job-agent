from typing import Dict, Any


def mock_analyze_cv(text: str, lang: str = 'he') -> Dict[str, Any]:
    if lang == 'en':
        return {"score": 80, "summary": "Mock CV summary", "suggestions": ["Highlight achievements", "Shorten paragraphs"], "bullets": ["Improve bullet X", "Add skills"]}
    return {"score": 80, "summary": "CV summary mock", "suggestions": ["הדגישי הישגים", "קצרי פסקאות"], "bullets": ["שפרי bullet X", "הוסיפי כישורים"]}


def mock_match_job(cv_text: str, job_desc: str, lang: str = 'he') -> Dict[str, Any]:
    if lang == 'en':
        return {"match_score": 70, "common_terms": ["example"], "recommended_changes": ["add keyword"], "cover_letter": "Hello, I am interested..."}
    return {"match_score": 70, "common_terms": ["example"], "recommended_changes": ["הוסף מילת מפתח"], "cover_letter": "שלום, אני מעוניינת..."}


def mock_simulate_interview(title: str, lang: str = 'he') -> Dict[str, Any]:
    if lang == 'en':
        return {"questions": [f"Tell me about your experience for {title}"], "advice": "Answer briefly, with examples"}
    return {"questions": [f"ספרי על ניסיון ל-{title}"], "advice": "תשיבי בקצרה, עם דוגמאות"}
