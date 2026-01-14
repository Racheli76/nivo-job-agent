from typing import Any
from services.openai import call_openai_chat


def build_analyze_cv_prompt(text: str, job_desc: str = '', lang: str = 'he') -> str:
    if lang == 'en':
        base_prompt = (
            "You are a world-class Resume Writer and Career Coach. Analyze the provided CV.\n"
            "RETURN ONLY A VALID JSON OBJECT. NO markdown, NO code blocks, NO backticks, NO extra text before or after JSON.\n\n"
            "REQUIRED JSON FIELDS (ALL 6 MUST BE PRESENT):\n"
            "1. 'score': Integer 0-100 (rate CV quality as-is)\n"
            "2. 'score_after_improvement': Integer 0-100 (estimated score if candidate implements improved_cv)\n"
            "3. 'summary': String with 2-3 punchy professional sentences\n"
            "4. 'suggestions': Array of exactly 5 strings (specific improvements)\n"
            "5. 'improved_cv': String with completely rewritten CV:\n"
            "   - Start with name and headline\n"
            "   - Use strong action verbs (Developed, Managed, Spearheaded, Optimized, Engineered, Launched, Accelerated, Transformed)\n"
            "   - Include quantified metrics for every achievement (e.g., 'Increased X by 30%', 'Reduced Y by $50K', 'Led team of 8')\n"
            "   - Format with clear bullet points\n"
            "   - Make ATS-friendly (no tables, no special characters)\n"
            "   - Keep same contact details, enhance all experience descriptions\n"
            "6. 'cover_letter': String with professional cover letter (2-3 paragraphs, warm and engaging tone)"
        )
        
        if job_desc:
            return (
                base_prompt +
                f"\n\n*** JOB DESCRIPTION PROVIDED - REQUIRED ADDITIONAL FIELDS: ***\n"
                f"7. 'tailored_cv': STRING - Rewrite the improved_cv to match THIS specific job description.\n"
                f"   - Highlight skills and keywords from this job description\n"
                f"   - Reorganize experience to show most relevant roles first\n"
                f"   - Use same terminology and keywords from job posting\n"
                f"   - Make the candidate appear as perfect match for this job\n"
                f"8. 'missing_skills': ARRAY - List skills/requirements from job description NOT found in CV\n\n"
                f"JOB DESCRIPTION:\n{job_desc}\n\n"
                f"CV TEXT:\n{text}\n\n"
                "STRICT INSTRUCTIONS:\n"
                "- Return ONLY valid JSON (no markdown)\n"
                "- Include all 8 fields when job_desc is provided\n"
                "- Do not include any text outside the JSON object\n"
                "- Ensure tailored_cv is substantively different from improved_cv and job-specific\n"
                "- score_after_improvement should reflect boost from implementing improved_cv"
            )
        else:
            return (
                base_prompt +
                f"\n\nCV TEXT:\n{text}\n\n"
                "STRICT INSTRUCTIONS:\n"
                "- Return ONLY valid JSON (no markdown)\n"
                "- Include all 6 fields\n"
                "- Do not include any text outside the JSON object\n"
                "- score_after_improvement should be 15-25 points higher than score if improvements are solid"
            )
    else:
        base_prompt = (
            "אתה יועץ קריירה וכותב קורות חיים מעולם. נתח את קורות החיים המסופקות.\n"
            "החזר רק JSON תקני. ללא markdown, ללא backticks, ללא טקסט נוסף לפני או אחרי JSON.\n\n"
            "שדות JSON נדרשים (כל 6 חייבים להיות present):\n"
            "1. 'score': מספר שלם 0-100 (דרוג איכות קו\"ח כעת)\n"
            "2. 'score_after_improvement': מספר שלם 0-100 (ניקוד משוער אם המועמד יישם את improved_cv)\n"
            "3. 'summary': מחרוזת עם 2-3 משפטים חדים ומקצועיים\n"
            "4. 'suggestions': מערך של בדיוק 5 מחרוזות (שיפורים ספציפיים)\n"
            "5. 'improved_cv': מחרוזת עם קו\"ח משופר לחלוטין:\n"
            "   - התחל עם שם וכותרת\n"
            "   - השתמש בפעלים חזקים (פיתח, ניהל, הוביל, אופטימל, יישם, השיק, האיץ, שנה)\n"
            "   - כלול מדדים כמותיים לכל הישג (לדוגמה: 'הגדל X ב-30%', 'חסך Y של 50 אלף', 'הנהיג צוות של 8')\n"
            "   - עצב עם נקודות ברורות\n"
            "   - עדכן להיות ידידותי ל-ATS (ללא טבלאות, ללא תווים מיוחדים)\n"
            "   - שמור פרטי יצירת קשר, שפר את כל תיאורי הניסיון\n"
            "6. 'cover_letter': מחרוזת עם מכתב מקדים מקצועי (2-3 פסקאות, טון חם ומעורר)"
        )
        
        if job_desc:
            return (
                base_prompt +
                f"\n\n*** סופקה תיאור משרה - שדות נוספים נדרשים: ***\n"
                f"7. 'tailored_cv': מחרוזת - כתוב מחדש את ה-improved_cv כדי להתאים למשרה ספציפית זו.\n"
                f"   - הדגש כישורים ומילות-מפתח מתיאור המשרה\n"
                f"   - ארגן מחדש ניסיון כדי להראות תפקידים רלוונטיים ביותר קודם\n"
                f"   - השתמש באותו שפה ומילות-מפתח מהפוסט\n"
                f"   - הפוך המועמד להיראות כהתאמה מושלמת לתפקיד\n"
                f"8. 'missing_skills': מערך - רשום כישורים/דרישות מתיאור המשרה שלא בקו\"ח\n\n"
                f"תיאור המשרה:\n{job_desc}\n\n"
                f"טקסט קורות חיים:\n{text}\n\n"
                "הוראות קשוחות:\n"
                "- החזר רק JSON תקני (ללא markdown)\n"
                "- כלול את כל 8 השדות כשסופקה job_desc\n"
                "- אל תכלול טקסט כלשהו מחוץ לאובייקט JSON\n"
                "- וודא ש-tailored_cv שונה משמעותית מ-improved_cv ספציפי למשרה\n"
                "- score_after_improvement צריך לשקף את הגדלת הניקוד מהשיפורים"
            )
        else:
            return (
                base_prompt +
                f"\n\nטקסט קורות חיים:\n{text}\n\n"
                "הוראות קשוחות:\n"
                "- החזר רק JSON תקני (ללא markdown)\n"
                "- כלול את כל 6 השדות\n"
                "- אל תכלול טקסט כלשהו מחוץ לאובייקט JSON\n"
                "- score_after_improvement צריך להיות גבוה יותר ב-15-25 נקודות מ-score אם השיפורים טובים"
            )


def build_match_job_prompt(cv_text: str, job_desc: str, lang: str = 'he') -> str:
    if lang == 'en':
        return (
            "You are a career coach and recruiter. Analyze how well the CV matches the job description.\n"
            "Respond in English ONLY with a JSON object containing:\n"
            "- 'match_score': Integer (0-100) how well the CV matches this job.\n"
            "- 'common_terms': Array of keywords found in both CV and job description.\n"
            "- 'missing_skills': Array of job requirements NOT found in the CV.\n"
            "- 'recommended_changes': Array of specific changes to make the CV more relevant.\n"
            "- 'cover_letter': A personalized, warm and professional cover letter (2-3 paragraphs) for this specific role.\n\n"
            "Respond ONLY with valid JSON. No markdown, no extra text.\n\nCV:\n" + cv_text + "\n\nJOB DESCRIPTION:\n" + job_desc
        )
    else:
        return (
            "אתה יועץ קריירה וגיוס. נתח כיצד קורות החיים תואמים את תיאור המשרה.\n"
            "הגב בעברית בלבד ב-JSON object המכיל:\n"
            "- 'match_score': מספר שלם (0-100) כיצד קורות החיים תואמים משרה זו.\n"
            "- 'common_terms': מערך של מילות-מפתח הנמצאות בקורות חיים וגם בתיאור המשרה.\n"
            "- 'missing_skills': מערך של דרישות משרה שלא נמצאות בקורות החיים.\n"
            "- 'recommended_changes': מערך של שינויים ספציפיים כדי להפוך את קורות החיים רלוונטיים יותר.\n"
            "- 'cover_letter': מכתב מקדים מותאם, חם ומקצועי (2-3 פסקאות) למשרה ספציפית זו.\n\n"
            "הגב רק ב-JSON תקני. ללא Markdown, ללא טקסט נוסף.\n\nקורות חיים:\n" + cv_text + "\n\nתיאור המשרה:\n" + job_desc
        )


def build_simulate_interview_prompt(role: str, cv_text: str = '', lang: str = 'he') -> str:
    if lang == 'en':
        return (
            "You are an experienced interviewer and hiring manager. Given a role and candidate CV (if available), create a realistic interview experience.\n"
            "Respond in English ONLY with a JSON object containing:\n"
            "- 'questions': Array of 8 challenging, role-specific interview questions.\n"
            "- 'advice': Short practical tips for succeeding in this interview (2-3 sentences).\n"
            "- 'common_pitfalls': Array of 3 common mistakes candidates make for this role.\n\n"
            "Respond ONLY with valid JSON. No markdown, no extra text.\n\nRole:\n" + role + ("\n\nCV:\n" + cv_text if cv_text else "")
        )
    else:
        return (
            "אתה מראיין מנוסה ומנהל גיוס. בהנתן תפקיד וקורות חיים של המועמד (אם זמינות), צור חווית ראיון ריאליסטית.\n"
            "הגב בעברית בלבד ב-JSON object המכיל:\n"
            "- 'questions': מערך של 8 שאלות ראיון מאתגרות וספציפיות לתפקיד.\n"
            "- 'advice': טיפים מעשיים קצרים להצלחה בראיון זה (2-3 משפטים).\n"
            "- 'common_pitfalls': מערך של 3 טעויות נפוצות שמועמדים עושים בתפקיד זה.\n\n"
            "הגב רק ב-JSON תקני. ללא Markdown, ללא טקסט נוסף.\n\nתפקיד:\n" + role + ("\n\nקורות חיים:\n" + cv_text if cv_text else "")
        )


def run_analyze_cv(text: str, job_desc: str = '', lang: str = 'he', max_tokens: int = 2000) -> Any:
    prompt = build_analyze_cv_prompt(text, job_desc, lang)
    return call_openai_chat([{'role': 'user', 'content': prompt}], max_tokens=max_tokens)


def run_match_job(cv_text: str, job_desc: str, lang: str = 'he', max_tokens: int = 600) -> Any:
    prompt = build_match_job_prompt(cv_text, job_desc, lang)
    return call_openai_chat([{'role': 'user', 'content': prompt}], max_tokens=max_tokens)


def run_simulate_interview(role: str, cv_text: str = '', lang: str = 'he', max_tokens: int = 800) -> Any:
    prompt = build_simulate_interview_prompt(role, cv_text, lang)
    return call_openai_chat([{'role': 'user', 'content': prompt}], max_tokens=max_tokens)
