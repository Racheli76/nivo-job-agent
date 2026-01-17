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
            "Respond in English ONLY with a JSON object containing EXACTLY these fields:\n"
            "- 'match_score': Integer (0-100) how well the CV matches this job.\n"
            "- 'score_after_improvement': Integer (0-100) estimated score if candidate uses tailored_cv.\n"
            "- 'common_skills': Array of skills/keywords found in BOTH CV and job description (things the candidate HAS).\n"
            "- 'required_skills': Array of all important skills/keywords from job description needed for this role.\n"
            "- 'missing_skills': Array of job requirements NOT found in the CV (what candidate needs to learn).\n"
            "- 'tailored_cv': String - FULL-LENGTH professional CV rewrite (minimum 1000 words) tailored to match this specific job. Maintain the same structure and length as the original CV with all sections intact (summary, achievements, technical skills, additional sections). Emphasize relevant skills while keeping ONLY what actually exists in the original CV. Use strong action verbs and quantified metrics. Reorganize and reframe existing experience to highlight job-relevant accomplishments. Do not invent skills or experience.\n"
            "- 'cover_letter': String - personalized, warm and professional cover letter (2-3 substantial paragraphs) for this specific role. Should be 300-400 words.\n"
            "- 'recommended_changes': Array of 3-4 specific, actionable changes to make the CV more relevant to this job.\n\n"
            "CRITICAL RULES:\n"
            "- tailored_cv must be FULL-LENGTH with complete sections from original CV, not abbreviated\n"
            "- tailored_cv must ONLY use skills/experience that actually exist in the provided CV\n"
            "- Do not invent or hallucinate qualifications\n"
            "- Maintain original CV structure: Professional Summary, Key Achievements, Technical Skills, and any other sections\n"
            "- Reorganize and reframe existing experience to match job requirements\n"
            "- score_after_improvement should be 10-15 points higher than match_score\n"
            "- Use job description keywords in cover_letter and tailored_cv\n"
            "- Respond ONLY with valid JSON. No markdown, no extra text.\n\n"
            "CV:\n" + cv_text + "\n\nJOB DESCRIPTION:\n" + job_desc
        )
    else:
        return (
            "אתה יועץ קריירה וגיוס מנוסה. נתח כיצד קורות החיים תואמים את תיאור המשרה.\n"
            "הגב בעברית בלבד ב-JSON object המכיל בדיוק את השדות הבאים:\n"
            "- 'match_score': מספר שלם (0-100) עד כמה קורות החיים תואמים משרה זו.\n"
            "- 'score_after_improvement': מספר שלם (0-100) ניקוד משוער אם המועמד משתמש ב-tailored_cv.\n"
            "- 'common_skills': מערך של כישורים/מילות-מפתח שנמצאות בקורות חיים וגם בתיאור משרה (דברים שיש למועמד).\n"
            "- 'required_skills': מערך של כל הכישורים החשובים/מילות-מפתח מתיאור המשרה הנדרשים לתפקיד זה.\n"
            "- 'missing_skills': מערך של דרישות משרה שלא נמצאות בקורות החיים (מה שמועמד צריך ללמוד).\n"
            "- 'tailored_cv': מחרוזת - שכתוב קורות חיים בעברית באורך מלא (מינימום 1000 מילים) המותאמות למשרה ספציפית זו. שמור על אותו מבנה ואורך של קורות החיים המקוריים עם כל הסעיפים שלמים (סיכום מקצועי, הישגים, כישורים טכניים, סעיפים נוספים). הדגש כישורים רלוונטיים תוך שמירה רק על מה שבאמת קיים בקורות החיים המקוריים. השתמש בפעלים חזקים ובמדדים כמותיים. סדרו מחדש והגדר מחדש ניסיון קיים כדי להדגיש הישגים הרלוונטיים למשרה. אל תמציא כישורים או ניסיון.\n"
            "- 'cover_letter': מחרוזת - מכתב מקדים מותאם, חם ומקצועי (2-3 פסקאות משמעותיות) למשרה ספציפית זו. צריך להיות 300-400 מילים.\n"
            "- 'recommended_changes': מערך של 3-4 שינויים ספציפיים וישימים כדי להפוך את קורות החיים רלוונטיים יותר למשרה זו.\n\n"
            "כללים קריטיים:\n"
            "- tailored_cv חייב להיות בעל אורך מלא עם סעיפים שלמים מקורות החיים המקוריים, לא מקוצר\n"
            "- tailored_cv חייב להשתמש רק בכישורים/ניסיון שבאמת קיימים בקורות החיים המסופקים\n"
            "- אל תמציא או תהלוצינציה כישורים או ניסיון\n"
            "- שמור על מבנה קורות החיים המקורי: סיכום מקצועי, הישגים מרכזיים, כישורים טכניים, וכל סעיף אחר\n"
            "- סדרו מחדש והגדירו מחדש ניסיון קיים כדי להתאים לדרישות המשרה\n"
            "- score_after_improvement צריך להיות 10-15 נקודות גבוה יותר מ-match_score\n"
            "- השתמש במילות-מפתח מתיאור המשרה ב-cover_letter וב-tailored_cv\n"
            "- הגב רק ב-JSON תקני. ללא Markdown, ללא טקסט נוסף.\n\n"
            "קורות חיים:\n" + cv_text + "\n\nתיאור המשרה:\n" + job_desc
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


def run_match_job(cv_text: str, job_desc: str, lang: str = 'he', max_tokens: int = 3000) -> Any:
    prompt = build_match_job_prompt(cv_text, job_desc, lang)
    return call_openai_chat([{'role': 'user', 'content': prompt}], max_tokens=max_tokens)


def run_simulate_interview(role: str, cv_text: str = '', lang: str = 'he', max_tokens: int = 800) -> Any:
    prompt = build_simulate_interview_prompt(role, cv_text, lang)
    return call_openai_chat([{'role': 'user', 'content': prompt}], max_tokens=max_tokens)
