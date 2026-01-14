from typing import Dict, Any


def mock_analyze_cv(text: str, lang: str = 'he', job_desc: str = '') -> Dict[str, Any]:
    if lang == 'en':
        result = {
            "score": 72,
            "score_after_improvement": 91,
            "summary": "Strong professional background with solid technical skills and proven leadership experience. CV demonstrates impact but needs better quantification and structure.",
            "suggestions": [
                "Add specific metrics and percentages to all achievements",
                "Use stronger action verbs to start each bullet point",
                "Reorganize experience section with most relevant role first",
                "Include a Professional Summary at the top",
                "Format as clean bullet points instead of paragraphs"
            ],
            "improved_cv": "JOHN SMITH\nSenior Software Engineer | Full-Stack Developer\n\nPROFESSIONAL SUMMARY\nResults-driven Senior Software Engineer with 8+ years architecting and scaling high-impact systems. Proven expertise leading cross-functional teams, delivering $2M+ in business value, and mentoring next-generation engineers.\n\nKEY ACHIEVEMENTS\n• Spearheaded architecture redesign reducing API response time by 50%, improving experience for 2M+ daily active users\n• Developed automated testing framework increasing code coverage from 45% to 92%, reducing production incidents by 65%\n• Managed team of 5+ junior engineers with 100% advancement rate within 24 months\n• Engineered microservices migration reducing deployment cycles by 70% and infrastructure costs by 40%\n• Optimized database queries improving system performance by 35% and reducing server load\n\nTECHNICAL SKILLS\nLanguages: Python, JavaScript, TypeScript, Go | Databases: PostgreSQL, MongoDB, Redis | Cloud: AWS, GCP, Kubernetes | Tools: Docker, CI/CD, Git",
            "cover_letter": "Dear Hiring Team,\n\nI am excited to apply for this position with my 8+ years of software engineering expertise. My background in designing scalable systems and leading high-performing teams aligns perfectly with your needs. I am confident that my technical skills and proven ability to deliver measurable business value will make me a strong asset to your organization.\n\nI look forward to discussing how I can contribute to your team's success."
        }
        # Add tailored_cv and missing_skills only when job_desc is provided
        if job_desc:
            result["score_after_improvement"] = 94
            result["tailored_cv"] = "JOHN SMITH\nSenior Software Engineer | Full-Stack Developer | Cloud Architecture Specialist\n\nPROFESSIONAL SUMMARY\nResults-driven Senior Software Engineer with 8+ years architecting and scaling high-impact cloud systems. Expert in microservices, Kubernetes, and cloud-native technologies (AWS, GCP). Proven expertise leading cross-functional teams, delivering $2M+ in business value, and mentoring next-generation engineers.\n\nKEY ACHIEVEMENTS\n• Spearheaded Kubernetes migration and microservices architecture redesign reducing API response time by 50%, improving experience for 2M+ daily active users\n• Developed automated testing framework increasing code coverage from 45% to 92%, reducing production incidents by 65%\n• Managed team of 5+ junior engineers with 100% advancement rate within 24 months\n• Engineered microservices migration reducing deployment cycles by 70% and infrastructure costs by 40%\n• Optimized database queries and cloud resources improving system performance by 35% and reducing cloud spend by 40%\n• Architected scalable solutions using AWS/GCP services for enterprise clients\n\nCLOUD & TECHNICAL EXPERTISE\nCloud Platforms: AWS (EC2, S3, Lambda, RDS), GCP (Comxxxx Engine, Cloud Storage) | Container Orchestration: Kubernetes, Docker | Languages: Python, JavaScript, TypeScript, Go | Databases: PostgreSQL, MongoDB, Redis | CI/CD & DevOps: Jenkins, GitHub Actions, GitLab CI"
            result["missing_skills"] = ["Terraform", "CloudFormation", "Prometheus monitoring"]
        return result
    else:
        result = {
            "score": 72,
            "score_after_improvement": 91,
            "summary": "רקע מקצועי חזק עם כישורים טכניים מוצקים וניסיון הנהגה מוכח. קורות חיים מדגימים השפעה אך זקוקים לכימות טוב יותר ומבנה.",
            "suggestions": [
                "הוסף מדדים ספציפיים ואחוזים לכל הישג",
                "השתמש בפעלים חזקים יותר בהתחלת כל bullet point",
                "ארגן מחדש סעיף ניסיון עם התפקיד הרלוונטי ביותר קודם",
                "כלול סיכום מקצועי בחלק העליון",
                "עצב כ-bullet points נקיים במקום פסקאות"
            ],
            "improved_cv": "יוחנן שמידט\nמהנדס תוכנה בכיר | מפתח Full-Stack\n\nסיכום מקצועי\nמהנדס תוכנה מוכוון תוצאות עם 8+ שנים בתכנון ויישום מערכות בהשפעה גבוהה. ניסיון מוכח בהובלת צוותים רוחביים, הסגת $2M+ בערך עסקי, והדרכת מהנדסי דור הבא.\n\nהישגים מרכזיים\n• הנהיג עיצוב מחדש של architecture שהפחית זמן תגובה ב-50%, שיפור חוויה עבור 2M+ משתמשים פעילים יומיים\n• פיתח מסגרת בדיקות אוטומטיות שהגבירה code coverage מ-45% ל-92%, והפחיתה תקלות בייצור ב-65%\n• ניהל צוות של 5+ מהנדסים צעירים עם שיעור קידום של 100% תוך 24 חודשים\n• יישם migration למיקרו-שירותים שהפחית מחזורי deployment ב-70% ועלויות infrastructure ב-40%\n• אופטימיזציה של שאילתות בסיס נתונים שיפרה ביצועי מערכת ב-35% והפחיתה עומס שרת\n\nכישורים טכניים\nשפות: Python, JavaScript, TypeScript, Go | מסדי נתונים: PostgreSQL, MongoDB, Redis | Cloud: AWS, GCP, Kubernetes | כלים: Docker, CI/CD, Git",
            "cover_letter": "צוות גיוס יקר,\n\nאני שמח להגיש מועמדות לתפקיד זה עם 8+ שנים של ניסיון בהנדסת תוכנה. הרקע שלי בעיצוב מערכות חסכוניות והנהגת צוותים בעלי ביצועים גבוהים תואם בדיוק את הצרכים שלכם. אני בטוח כי הכישורים הטכניים שלי והיכולת המוכחת שלי להשיג ערך עסקי משמעותי יהפכו אותי לנכס חזק בארגון שלכם.\n\nאני מצפה לדון כיצד אוכל לתרום להצלחת הצוות שלכם."
        }
        # Add tailored_cv and missing_skills only when job_desc is provided
        if job_desc:
            result["score_after_improvement"] = 94
            result["tailored_cv"] = "יוחנן שמידט\nמהנדס תוכנה בכיר | מפתח Full-Stack | מומחה ארכיטקטורה ענן\n\nסיכום מקצועי\nמהנדס תוכנה מוכוון תוצאות עם 8+ שנים בתכנון ויישום מערכות ענן בהשפעה גבוהה. מומחה בmicroservices, Kubernetes וטכנולוגיות cloud-native (AWS, GCP). ניסיון מוכח בהובלת צוותים רוחביים, הסגת $2M+ בערך עסקי, והדרכת מהנדסי דור הבא.\n\nהישגים מרכזיים\n• הנהיג migration ל-Kubernetes ועיצוב מחדש של microservices שהפחית זמן תגובה ב-50%\n• פיתח מסגרת בדיקות אוטומטיות שהגבירה code coverage מ-45% ל-92%\n• ניהל צוות של 5+ מהנדסים צעירים עם שיעור קידום של 100%\n• יישם migration למיקרו-שירותים שהפחית deployment cycles ב-70%\n• אופטימיזציה של משאבי ענן שהפחיתה עלויות ב-40%\n• ארכיטקט של פתרונות חסכוניים ב-AWS/GCP לקליינטים enterprise\n\nמומחיות ענן וטכנית\nפלטפורמות ענן: AWS (EC2, S3, Lambda, RDS), GCP | Orchestration: Kubernetes, Docker | שפות: Python, JavaScript, TypeScript, Go | מסדי נתונים: PostgreSQL, MongoDB, Redis | CI/CD: Jenkins, GitHub Actions"
            result["missing_skills"] = ["Terraform", "CloudFormation", "Prometheus"]
        return result


def mock_match_job(cv_text: str, job_desc: str, lang: str = 'he') -> Dict[str, Any]:
    if lang == 'en':
        return {"match_score": 70, "common_terms": ["example"], "recommended_changes": ["add keyword"], "cover_letter": "Hello, I am interested..."}
    return {"match_score": 70, "common_terms": ["example"], "recommended_changes": ["הוסף מילת מפתח"], "cover_letter": "שלום, אני מעוניינת..."}


def mock_simulate_interview(title: str, lang: str = 'he') -> Dict[str, Any]:
    if lang == 'en':
        return {"questions": [f"Tell me about your experience for {title}"], "advice": "Answer briefly, with examples"}
    return {"questions": [f"ספרי על ניסיון ל-{title}"], "advice": "תשיבי בקצרה, עם דוגמאות"}
