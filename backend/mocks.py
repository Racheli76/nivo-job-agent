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
        return {
            "match_score": 75,
            "score_after_improvement": 88,
            "common_skills": ["C#", "Windows", "Git"],
            "required_skills": ["C#", "Windows", "Git", "Azure", "Multi-Threading", "TCP/UDP", "WPF"],
            "missing_skills": ["Azure", "Multi-Threading", "TCP/UDP", "WPF"],
            "tailored_cv": "SOFTWARE DEVELOPER NAME\nSenior Software Engineer | C# Specialist | Windows Desktop & Systems Development Expert\n\nPROFESSIONAL SUMMARY\nSeasoned software engineer with extensive experience developing robust Windows-based applications using C#. Deep expertise in WPF user interface development, system-level programming, and network communication protocols. Proven track record of delivering high-performance solutions in security-focused environments with emphasis on reliability and optimization. Strong background in Git-based collaborative development and multi-threading architecture implementation.\n\nKEY ACCOMPLISHMENTS\n• Designed and developed multiple Windows Desktop applications using C# with advanced WPF user interfaces and complex state management\n• Implemented sophisticated Multi-Threading solutions that increased system performance by up to 50% in security-critical applications\n• Built and maintained TCP/UDP-based network communication systems ensuring 99.9% uptime and reliable message delivery\n• Architected Asynchronous programming patterns using async/await and Task Parallel Library for responsive applications\n• Led code reviews and maintained high quality standards through Git-based workflows in team environments of 5+ developers\n• Integrated Azure cloud services to existing desktop applications, achieving improved scalability and reduced infrastructure costs\n• Contributed to long-term maintenance and enhancement of complex security domain systems with millions of lines of code\n• Optimized memory usage and application performance, reducing resource consumption by 35% in critical operations\n\nTECHNICAL SKILLS & EXPERTISE\nProgramming Languages: C# (Expert) | UI Frameworks: WPF (Advanced), Winforms | Platforms: Windows (Desktop, Server, Services) | Networking: TCP, UDP, Socket Programming, Async Sockets | Concurrency: Multi-Threading, Thread Pools, Async/Await, Task Parallel Library, Cancellation Tokens | Version Control: Git (Advanced), GitHub, GitLab workflows | Cloud Platforms: Azure (VMs, App Services, SQL Database) | Database: SQL Server, Entity Framework | Development Practices: Agile/Scrum, Code Reviews, Unit Testing, TDD, Design Patterns\n\nSPECIAL CAPABILITIES\n• Deep understanding of real-time data processing and handling mission-critical systems\n• Expertise in designing responsive applications handling heavy computational workloads\n• Advanced knowledge of secure network communication and data protection protocols\n• Proficiency in debugging complex multi-threaded applications and race condition identification\n• Experience working in security-focused domains with strict performance and reliability requirements",
            "cover_letter": "Dear Hiring Manager,\n\nI am writing to express my strong interest in the Software Engineer position at your esteemed organization. With extensive experience developing high-performance Windows applications using C# and proven expertise in WPF, multi-threading, and cloud technologies, I am confident that I can make significant contributions to your team.\n\nThroughout my career, I have demonstrated a commitment to delivering robust, scalable solutions. My proficiency in TCP/UDP network programming, combined with hands-on experience integrating Azure services, positions me exceptionally well to address your technical needs. I have consistently delivered solutions that improved system performance by 35-50%, and I take pride in maintaining the highest code quality standards through rigorous Git-based workflows and comprehensive testing practices.\n\nMy background in security-focused environments has equipped me with deep understanding of mission-critical system requirements and the discipline needed to ensure reliability and optimization. I am particularly drawn to your organization because of its commitment to technical excellence and innovation, and I am excited about the opportunity to contribute my skills and experience to your team's continued success.\n\nI would welcome the opportunity to discuss how my experience in designing scalable Windows applications, implementing complex multi-threaded architectures, and integrating cloud solutions aligns with your team's objectives. Thank you for considering my application.",
            "recommended_changes": [
                "Highlight specific WPF projects and frameworks used",
                "Add examples of multi-threading implementations with performance metrics",
                "Include Azure cloud certifications or hands-on experience",
                "Emphasize network programming experience with TCP/UDP protocols"
            ]
        }
    else:
        return {
            "match_score": 75,
            "score_after_improvement": 88,
            "common_skills": ["C#", "Windows", "Git"],
            "required_skills": ["C#", "Windows", "Git", "Azure", "Multi-Threading", "TCP/UDP", "WPF"],
            "missing_skills": ["Azure", "Multi-Threading", "TCP/UDP", "WPF"],
            "tailored_cv": "שם מפתח\nמהנדס תוכנה בכיר | מומחה C# ו-Windows | מיוחד ב-WPF ורשתות\n\nסיכום מקצועי\nמהנדס תוכנה ממוקד תוצאות עם ניסיון רחב בפיתוח אפליקציות מערכתיות בשפת C# ובסביבת Windows. בעל ניסיון מעמיק בפיתוח ממשקי משתמש בעזרת WPF, תכנות מובנה וממשקי הודעות. מומחה בהטמעת פתרונות רשתיים באמצעות TCP/UDP והבנה עמוקה של Multi-Threading וAsynchronous programming.\n\nהישגים עיקריים\n• פיתח מספר יישומי Windows Desktop בתוך C# המשתמשים בWPF עם ממשקי משתמש מתקדמים\n• יישם מערכות Multi-Threading לשיפור ביצועים ל-50% במערכות בתחום הבטחוני\n• פעל עם פרוטוקולי TCP/UDP לתקשורת בין רכיבים, מה שהביא לשיפור יציבות המערכת ב-40%\n• פיתח רכיבים קריטיים בעבודה עם Asynchronous patterns ודוגמאות Multi-Tasking\n• עבד בצוותים מופעלים Git עם סטנדרטים גבוהים של Code Review ובדיקות איכות\n• משלב Azure services בפרויקטים קיימים כדי להשיג סקלביליות גבוהה וביצועים משופרים\n• התרומה לתחזוקה ופיתוח מערכות מורכבות בתחום ביטחוני במשך שנים\n\nכישורים וניסיון טכני\nשפות: C# (עמוק) | GUI Frameworks: WPF (מיוחד) | סביבה: Windows (Desktop, Server) | Networking: TCP, UDP, Socket Programming | Threading: Multi-Threading, Async/Await, Task Parallel Library | Version Control: Git (advanced) | Cloud: Azure (hands-on) | Development Practices: Agile, Code Reviews, Unit Testing\n\nיכולות מיוחדות\n• פיתוח יישומים לתחום הביטחוני עם הקפדה על ביטחון וביצועים\n• יכולת עבודה בפרויקטים מורכבים דורשים Multi-Threading ו-Real-time processing\n• חוכמת טכנית בהטמעת תקשורת רשתית יעילה ובטוחה\n• ניסיון בשימוש בGit בסביבות צוות גדולות עם workflow מקצועי",
            "cover_letter": "מנהל גיוס יקר,\n\nאני שמח להגיש מועמדות לתפקיד מהנדס תוכנה בכיר בארגון שלכם. עם ניסיון של מעל שנים בפיתוח יישומי Windows בעזרת C#, מומחיות עמוקה בWPF, וידע מעמיק בארכיטקטורות מערכתיות, אני בטוח ביכולתי לתרום בצורה משמעותית וממיידית לצוות ההנדסה שלכם.\n\nלאורך קריירתי, הדגמתי התחייבות למספק פתרונות חזקים וסקלביים. הופעתי בתכנות TCP/UDP רשת, בשילוב עם ניסיון ידני בintegration שירותי Azure, מעמדים אותי בצורה יוצאת דופן כדי לתמוך בצרכים הטכניים שלכם. הסגתי בעקביות פתרונות ששיפרו ביצועי מערכות ב-35-50%, ואני גאה בשמירה על סטנדרטים אמת של איכות קוד דרך תהליכי Git קפדניים והנסות בדיקה כוללות.\n\nהרקע שלי בסביבות ממוקדות בביטחון הצייד אותי בהבנה עמוקה של דרישות מערכות קריטיות משימה והמשמעת הנדרשת כדי להבטיח אמינות והנדסה. אני מיוחד למשוך לארגון שלכם בגלל התחייבותו לעלות טכנית וחדשנות, והנני שמח על ההזדמנות לתרום את הכישורים והניסיון שלי להצלחה ממשיכה של צוות שלכם.\n\nהייתי שמח על ההזדמנות לדון איך הניסיון שלי בתכנון יישומי Windows חסכוניים, יישום ארכיטקטורות Multi-Threaded מורכבות, וintegration פתרונות ענן תואמים את יעדי הצוות שלכם. תודה על בחינת הבקשה שלי.",
            "recommended_changes": [
                "הדגש פרויקטי WPF ספציפיים וממסגרות שנעשה בהם שימוש",
                "הוסף דוגמאות ליישומי Multi-Threading עם מדדי ביצועים",
                "כלול הסמכות Azure או ניסיון ישיר בענן",
                "הדגש ניסיון בתכנות רשת עם פרוטוקולי TCP/UDP"
            ]
        }


def mock_simulate_interview(title: str, lang: str = 'he') -> Dict[str, Any]:
    if lang == 'en':
        return {"questions": [f"Tell me about your experience for {title}"], "advice": "Answer briefly, with examples"}
    return {"questions": [f"ספרי על ניסיון ל-{title}"], "advice": "תשיבי בקצרה, עם דוגמאות"}
