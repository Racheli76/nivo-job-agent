
import React from 'react';
import './index.css';
import NivoImg from './nivo.png';
import { createRoot } from 'react-dom/client';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000';

function pretty(data) {
  try { return JSON.stringify(data, null, 2); }
  catch (e) { return String(data); }
}

function App() {
  // --- State ---
  const [step, setStep] = React.useState(0); // 0: Upload, 1: Job, 2: Results
  const [cvText, setCvText] = React.useState('');
  const [jobDesc, setJobDesc] = React.useState('');
  const [isProcessing, setIsProcessing] = React.useState(false);
  const [result, setResult] = React.useState(null);
  const [error, setError] = React.useState(null);
  const [nivoAnim, setNivoAnim] = React.useState('idle'); // idle | thinking | success
  const [sessionId, setSessionId] = React.useState(null);
  const [sessionLang, setSessionLang] = React.useState(null);
  const [language, setLanguage] = React.useState('he');
  const [healthStatus, setHealthStatus] = React.useState('unknown');
  const [coverLetter, setCoverLetter] = React.useState(null);
  const [interview, setInterview] = React.useState(null); // {questions: [], advice: ''}
  const fileInput = React.useRef();

  // --- Translations ---
  const translations = {
    he: {
      agentName: 'ניבו',
      tagline: 'הסנאי האסטרטגי שמלווה אותך',
          startBtn: 'העלאת קובץ',
      nextBtn: 'הבא',
      backBtn: 'חזרה',
      stepUpload: 'העלאת קורות חיים',
      stepJob: 'תיאור משרה',
      stepResult: 'תוצאה',
      uploadPlaceholder: 'הדביקי או העלי קובץ קורות חיים',
      jobPlaceholder: 'הדביקי תיאור משרה',
      analyzeBtn: 'נתח קובץ',
      matchBtn: 'בדוק התאמה',
      simulateBtn: 'התחל סימולציה',
      needCv: 'אנא הוסיפי קורות חיים כדי להמשיך',
      needJob: 'אנא הוסיפי תיאור משרה כדי להמשיך',
          restart: 'נתחי קובץ נוסף',
          finishBtn: 'סיים',
          tryAgainBtn: 'נסה שוב',
    },
    en: {
      agentName: 'Nivo',
      tagline: 'Your strategic squirrel guide',
          startBtn: 'Upload CV',
      nextBtn: 'Next',
      backBtn: 'Back',
      stepUpload: 'Upload CV',
      stepJob: 'Job Details',
      stepResult: 'Result',
      uploadPlaceholder: 'Paste or upload your CV',
      jobPlaceholder: 'Paste job description',
      analyzeBtn: 'Analyze CV',
      matchBtn: 'Check Match',
      simulateBtn: 'Start Simulation',
      needCv: 'Please add a CV to continue',
      needJob: 'Please add a job description to continue',
          restart: 'Analyze another file',
          finishBtn: 'Finish',
          tryAgainBtn: 'Try Again',
    }
  };
  const t = translations[language];

  // --- API Calls ---
  async function uploadFile(e) {
    const f = e.target.files?.[0];
    if (!f) return;
    setIsProcessing(true);
    setNivoAnim('thinking');
    try {
      const form = new FormData(); form.append('file', f);
      const res = await fetch(`${API_BASE}/upload-cv-file`, { method: 'POST', body: form });
      const data = await res.json();
      setCvText(data.text_preview || '');
      if (data.session_id) setSessionId(data.session_id);
      if (data.lang) setSessionLang(data.lang);
      setTimeout(() => setNivoAnim('success'), 200);
      setTimeout(() => setNivoAnim('idle'), 1200);
      setStep(1);
    } catch (err) {
      const text = await f.text().catch(() => '');
      setCvText(text);
      setError('שגיאה בקריאת קובץ');
    } finally {
      setIsProcessing(false);
    }
  }

  // Create a session on the server from raw pasted text by uploading a synthetic file.
  async function createSessionFromText(text) {
    if (!text || !text.trim()) return null;
    try {
      const blob = new Blob([text], { type: 'text/plain' });
      const file = new File([blob], 'pasted-cv.txt', { type: 'text/plain' });
      const form = new FormData();
      form.append('file', file);
      const res = await fetch(`${API_BASE}/upload-cv-file`, { method: 'POST', body: form });
      const data = await res.json();
      if (data.session_id) {
        setSessionId(data.session_id);
        if (data.lang) setSessionLang(data.lang);
      }
      return data.session_id || null;
    } catch (e) {
      console.error('createSessionFromText failed', e);
      return null;
    }
  }

  // Ensure we have a session_id before calling other endpoints. If missing, create from cvText.
  async function ensureSession() {
    if (sessionId) return sessionId;
    if (!cvText || !cvText.trim()) return null;
    return await createSessionFromText(cvText);
  }

  async function analyze() {
    setError(null);
    setIsProcessing(true);
    setNivoAnim('thinking');
    // ensure session is present so backend has the CV stored
    await ensureSession();
    try {
      const body = { text: cvText };
      if (sessionId) body.session_id = sessionId;
      if (jobDesc && jobDesc.trim()) body.job_desc = jobDesc;
      const res = await fetch(`${API_BASE}/analyze-cv`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
      const data = await res.json();
      setResult(data.result || data);
      // clear specialized outputs
      setCoverLetter(null);
      setInterview(null);
      setTimeout(() => setNivoAnim('success'), 200);
      setTimeout(() => setNivoAnim('idle'), 1200);
      setStep(2);
    } catch (e) {
      setError(String(e));
    } finally {
      setIsProcessing(false);
    }
  }

  async function matchJob() {
    setError(null);
    setIsProcessing(true);
    setNivoAnim('thinking');
    // ensure session so backend can access stored CV
    await ensureSession();
    try {
      const body = { title: '', description: jobDesc };
      if (sessionId) body.session_id = sessionId;
      const res = await fetch(`${API_BASE}/match-job`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
      const data = await res.json();
      const payload = data.result || data;
      setResult(payload);
      // extract cover letter when available
      if (payload && typeof payload === 'object') {
        setCoverLetter(payload.cover_letter || payload.coverLetter || null);
      } else {
        setCoverLetter(null);
      }
      setInterview(null);
      setTimeout(() => setNivoAnim('success'), 200);
      setTimeout(() => setNivoAnim('idle'), 1200);
      setStep(2);
    } catch (e) {
      setError(String(e));
    } finally {
      setIsProcessing(false);
    }
  }

  async function simulate() {
    setError(null);
    setIsProcessing(true);
    setNivoAnim('thinking');
    // ensure session so simulation can use stored CV
    await ensureSession();
    try {
      const role = 'Role';
      const form = new FormData();
      const titlePayload = sessionId ? `${role}||${sessionId}` : role;
      form.append('title', titlePayload);
      // also send session_id explicitly (backend supports session via title parsing)
      if (sessionId) form.append('session_id', sessionId);
      const res = await fetch(`${API_BASE}/simulate-interview`, { method: 'POST', body: form });
      const dataRaw = await res.json();
      const payload = dataRaw.result || dataRaw;
      // payload should contain questions and advice
      setInterview(payload || null);
      setResult(payload || null);
      setCoverLetter(null);
      setStep(2);
      setTimeout(() => setNivoAnim('success'), 200);
      setTimeout(() => setNivoAnim('idle'), 1200);
    } catch (e) {
      setError(String(e));
    } finally {
      setIsProcessing(false);
    }
  }

  async function decide() {
    if (!sessionId) {
      // try to create one from pasted CV if available
      await ensureSession();
      if (!sessionId) return;
    }
    setError(null);
    setIsProcessing(true);
    setNivoAnim('thinking');
    try {
      const res = await fetch(`${API_BASE}/decide`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ session_id: sessionId }) });
      const data = await res.json();
      setResult(data || null);
      // backend returns { action: 'prep_interview'|'improve_cv', match_score }
      const action = data && data.action;
      if (action === 'prep_interview') {
        // run simulate flow
        await simulate();
      } else if (action === 'improve_cv') {
        // run match job to generate recommended changes / cover letter
        await matchJob();
      }
      setTimeout(() => setNivoAnim('success'), 200);
      setTimeout(() => setNivoAnim('idle'), 1200);
    } catch (e) {
      setError(String(e));
    } finally {
      setIsProcessing(false);
    }
  }

  // --- Stepper Dots ---
  const steps = [t.stepUpload, t.stepJob, t.stepResult];

  // --- Health Check ---
  async function checkHealth() {
    try {
      const res = await fetch(`${API_BASE}/health`);
      const data = await res.json();
      setHealthStatus(data.status || 'ok');
    } catch (e) {
      setHealthStatus('down');
    }
  }

  React.useEffect(() => { checkHealth(); }, []);

  // --- UI ---
  return (
    <div id="root" dir={language === 'he' ? 'rtl' : 'ltr'}>
      <div className="app-container">
        {/* Nivo Character - always visible, never inside a card */}
        <div className="nivo-stage">
          <img
            src={NivoImg}
            alt="Nivo the Agent"
            className={`nivo-img ${nivoAnim}`}
            draggable={false}
            style={{ userSelect: "none" }}
          />
        </div>

        {/* Main Content Card */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: language === 'he' ? 'flex-start' : 'flex-end', gap: 12, marginBottom: 16 }}>
            <div style={{ alignSelf: 'center', color: 'var(--muted)', fontSize: 13 }}>API: {healthStatus}</div>
            <button className="btn secondary" onClick={() => { setLanguage(language === 'he' ? 'en' : 'he'); }}>
              {language === 'he' ? 'EN' : 'עברית'}
            </button>
            <button className="btn secondary" onClick={checkHealth} title="Refresh health">Refresh</button>
          </div>
          {/* Brand / Header */}
          <div className="brand">
            <div className="brand-left">
              <div className="brand-logo">NIVO</div>
              <div className="brand-sub">{t.agentName} — {t.tagline}</div>
            </div>
            <div className="brand-desc muted">
              {language === 'he' ? 'סנאי אסטרטגי שמנתח קורות חיים, משפר אותם ומכין אותך לראיון.' : 'Your strategic squirrel: analyzes CVs, refines them and preps you for interviews.'}
            </div>
          </div>

          {/* Stepper */}
          <div className="step-indicator">
            {steps.map((label, i) => (
              <div
                key={i}
                className={"step-dot" + (step === i ? " active" : "")}
                title={label}
              />
            ))}
          </div>

          {/* Step 0: Upload CV */}
          {step === 0 && (
            <div className="fade-in">
              <h1>{t.stepUpload}</h1>
              <input
                type="file"
                accept=".pdf,.doc,.docx,.txt"
                style={{ display: "none" }}
                ref={fileInput}
                onChange={uploadFile}
              />
              <button className="btn" onClick={() => fileInput.current.click()} disabled={isProcessing}>
                {t.startBtn}
              </button>
              <div style={{ marginTop: 30, color: "var(--text-muted)" }}>
                או הדביקי טקסט:
              </div>
              <textarea
                rows={6}
                placeholder={t.uploadPlaceholder}
                value={cvText}
                onChange={e => setCvText(e.target.value)}
                style={{ marginTop: 10 }}
                disabled={isProcessing}
              />
              <button
                className="btn"
                style={{ marginTop: 20 }}
                disabled={!cvText.trim() || isProcessing}
                onClick={async () => {
                  if (!sessionId && cvText && cvText.trim()) {
                    setIsProcessing(true);
                    setNivoAnim('thinking');
                    await ensureSession();
                    setIsProcessing(false);
                    setTimeout(() => setNivoAnim('success'), 150);
                    setTimeout(() => setNivoAnim('idle'), 1000);
                  }
                  setStep(1);
                }}
              >
                {t.nextBtn}
              </button>
            </div>
          )}

          {/* Step 1: Job Description / Decision Center */}
          {step === 1 && (
            <div className="fade-in">
              <h1>{t.stepJob}</h1>
              <textarea
                rows={5}
                placeholder={t.jobPlaceholder}
                value={jobDesc}
                onChange={e => setJobDesc(e.target.value)}
                disabled={isProcessing}
              />

              <div style={{ display: 'flex', gap: 10, marginTop: 18 }}>
                <button className="btn secondary" onClick={() => setStep(0)} disabled={isProcessing}>{t.backBtn}</button>
              </div>

              <div style={{ marginTop: 18 }}>
                <div style={{ fontWeight: 800, marginBottom: 8 }}>{language === 'he' ? 'Decision Center' : 'Decision Center'}</div>
                <div className="decision-grid">
                  <div className="decision-card">
                    <div style={{ fontWeight: 800 }}>{language === 'he' ? 'התאמה למשרה' : 'Match & Optimize'}</div>
                    <div className="muted" style={{ marginTop: 8 }}>{language === 'he' ? 'קבל מכתב מקדים ושינויים מומלצים' : 'Get cover letter & recommended changes'}</div>
                    <div style={{ marginTop: 12 }}>
                      <button className="btn" onClick={matchJob} disabled={isProcessing || !jobDesc.trim()}>{t.matchBtn}</button>
                    </div>
                  </div>

                  <div className="decision-card">
                    <div style={{ fontWeight: 800 }}>{language === 'he' ? 'הכנה לראיון' : 'Interview Prep'}</div>
                    <div className="muted" style={{ marginTop: 8 }}>{language === 'he' ? 'תרגול שאלות ועצות' : 'Practice questions & advice'}</div>
                    <div style={{ marginTop: 12 }}>
                      <button className="btn" onClick={simulate} disabled={isProcessing || !jobDesc.trim()}>{t.simulateBtn}</button>
                    </div>
                  </div>

                  <div className="decision-card">
                    <div style={{ fontWeight: 800 }}>{language === 'he' ? 'NIVO מקבל החלטה' : 'Let the Brain Decide'}</div>
                    <div className="muted" style={{ marginTop: 8 }}>{language === 'he' ? 'החלטה חכמה: ראיון או שיפור קורות חיים' : 'Decide: interview prep or CV improvement'}</div>
                    <div style={{ marginTop: 12 }}>
                      <button className="btn" onClick={decide} disabled={isProcessing || !jobDesc.trim()}>{language === 'he' ? 'הפעל' : 'Run'}</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Results */}
          {step === 2 && (
            <div className="fade-in">
              <h1>{t.stepResult}</h1>
              {result && (
                <div style={{ marginBottom: 20 }} className="result-panel">
                  {typeof result === 'string' ? (
                    <div style={{ whiteSpace: 'pre-wrap' }}>{result}</div>
                  ) : (
                    <>
                      <div style={{ fontSize: 22, fontWeight: 700, marginBottom: 8 }}>{result.summary || result.title || (language==='he' ? 'תוצאה' : 'Result')}</div>
                      
                      {/* Score Comparison */}
                      {(result.score != null || result.score_after_improvement != null) && (
                        <div style={{ marginTop: 16, padding: 12, backgroundColor: 'rgba(59, 130, 246, 0.1)', borderRadius: 8, border: '1px solid rgba(59, 130, 246, 0.3)' }}>
                          <div style={{ display: 'flex', gap: 24, justifyContent: 'center', alignItems: 'center' }}>
                            <div style={{ textAlign: 'center' }}>
                              <div style={{ fontSize: 12, color: 'var(--muted)', marginBottom: 4 }}>{language === 'he' ? 'ניקוד נוכחי' : 'Current Score'}</div>
                              <div style={{ fontSize: 28, fontWeight: 700, color: '#f59e0b' }}>{result.score || 0}</div>
                            </div>
                            <div style={{ fontSize: 24, color: 'var(--muted)' }}>→</div>
                            <div style={{ textAlign: 'center' }}>
                              <div style={{ fontSize: 12, color: 'var(--muted)', marginBottom: 4 }}>{language === 'he' ? 'ניקוד אחרי שיפור' : 'After Improvement'}</div>
                              <div style={{ fontSize: 28, fontWeight: 700, color: '#10b981' }}>{result.score_after_improvement || result.score || 0}</div>
                            </div>
                            {result.score_after_improvement && result.score && (
                              <div style={{ textAlign: 'center' }}>
                                <div style={{ fontSize: 12, color: 'var(--muted)', marginBottom: 4 }}>{language === 'he' ? 'שיפור' : 'Improvement'}</div>
                                <div style={{ fontSize: 28, fontWeight: 700, color: '#06b6d4' }}>+{result.score_after_improvement - result.score}</div>
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                      
                      {result.match_score != null && <div className="match-score-badge">{result.match_score}%</div>}
                      {result.common_terms && (
                        <div style={{ marginTop: 8 }}><strong>{language === 'he' ? 'מונחים משותפים:' : 'Common terms:'}</strong> {(result.common_terms || []).join(', ')}</div>
                      )}
                      {result.recommended_changes && (
                        <div style={{ marginTop: 8 }}>
                          <strong>{language === 'he' ? 'שינויים מומלצים:' : 'Recommended changes:'}</strong>
                          <ul style={{ textAlign: language === 'he' ? 'right' : 'left', direction: language === 'he' ? 'rtl' : 'ltr' }}>
                            {result.recommended_changes.map((c, i) => <li key={i}>{c}</li>)}
                          </ul>
                        </div>
                      )}
                      {result.suggestions && (
                        <div style={{ marginTop: 8 }}>
                          <strong>{language === 'he' ? 'הצעות לשיפור:' : 'Suggestions:'}</strong>
                          <ul style={{ textAlign: language === 'he' ? 'right' : 'left', direction: language === 'he' ? 'rtl' : 'ltr' }}>
                            {result.suggestions.map((s, i) => <li key={i}>{s}</li>)}
                          </ul>
                        </div>
                      )}

                      {/* Improved CV TextArea */}
                      {result.improved_cv && (
                        <div style={{ marginTop: 16 }}>
                          <div style={{ fontSize: 14, fontWeight: 700, marginBottom: 8 }}>{language === 'he' ? 'קורות חיים משופרים' : 'Improved CV'}</div>
                          <textarea
                            readOnly
                            value={result.improved_cv}
                            style={{
                              width: '100%',
                              height: 200,
                              padding: 12,
                              fontFamily: 'monospace',
                              fontSize: 12,
                              border: '1px solid var(--border-color)',
                              borderRadius: 6,
                              backgroundColor: 'rgba(0, 0, 0, 0.05)',
                              resize: 'vertical'
                            }}
                          />
                          <button
                            className="btn secondary"
                            style={{ marginTop: 8 }}
                            onClick={() => {
                              navigator.clipboard.writeText(result.improved_cv);
                              alert(language === 'he' ? 'הועתק ללוח!' : 'Copied to clipboard!');
                            }}
                          >
                            {language === 'he' ? 'העתק' : 'Copy'}
                          </button>
                        </div>
                      )}

                      {/* Tailored CV TextArea - only if job_desc was provided */}
                      {result.tailored_cv && (
                        <div style={{ marginTop: 16 }}>
                          <div style={{ fontSize: 14, fontWeight: 700, marginBottom: 8 }}>{language === 'he' ? 'קורות חיים מותאמים למשרה' : 'Tailored CV for Job'}</div>
                          <textarea
                            readOnly
                            value={result.tailored_cv}
                            style={{
                              width: '100%',
                              height: 200,
                              padding: 12,
                              fontFamily: 'monospace',
                              fontSize: 12,
                              border: '1px solid var(--border-color)',
                              borderRadius: 6,
                              backgroundColor: 'rgba(34, 197, 94, 0.05)',
                              resize: 'vertical'
                            }}
                          />
                          <button
                            className="btn secondary"
                            style={{ marginTop: 8 }}
                            onClick={() => {
                              navigator.clipboard.writeText(result.tailored_cv);
                              alert(language === 'he' ? 'הועתק ללוח!' : 'Copied to clipboard!');
                            }}
                          >
                            {language === 'he' ? 'העתק' : 'Copy'}
                          </button>
                        </div>
                      )}

                      {/* Missing Skills */}
                      {result.missing_skills && result.missing_skills.length > 0 && (
                        <div style={{ marginTop: 12 }}>
                          <strong>{language === 'he' ? 'כישורים חסרים:' : 'Missing skills:'}</strong>
                          <ul style={{ textAlign: language === 'he' ? 'right' : 'left', direction: language === 'he' ? 'rtl' : 'ltr' }}>
                            {result.missing_skills.map((skill, i) => <li key={i}>{skill}</li>)}
                          </ul>
                        </div>
                      )}
                    </>
                  )}

                  {coverLetter && (
                    <div style={{ marginTop: 12 }}>
                      <div style={{ fontWeight: 800 }}>{language === 'he' ? 'מכתב מקדים' : 'Cover Letter'}</div>
                      <pre style={{ whiteSpace: 'pre-wrap', margin: 0 }}>{coverLetter}</pre>
                    </div>
                  )}

                  {interview && (
                    <div style={{ marginTop: 12 }}>
                      <div style={{ fontWeight: 800 }}>{language === 'he' ? 'הכנה לראיון' : 'Interview Prep'}</div>
                      {interview.questions && (
                        <ol style={{ textAlign: language === 'he' ? 'right' : 'left', direction: language === 'he' ? 'rtl' : 'ltr' }}>
                          {interview.questions.map((q, i) => <li key={i}>{q}</li>)}
                        </ol>
                      )}
                      {interview.advice && (<div style={{ marginTop: 8, fontStyle: 'italic' }}>{interview.advice}</div>)}
                    </div>
                  )}

                  <div style={{ display: 'flex', gap: 10, marginTop: 16 }}>
                    <button className="btn" onClick={() => { setStep(0); setCvText(''); setJobDesc(''); setResult(null); setSessionId(null); setCoverLetter(null); setInterview(null); }}>
                      {t.finishBtn}
                    </button>
                    <button className="btn secondary" onClick={() => { setStep(0); setResult(null); setCoverLetter(null); setInterview(null); }}>
                      {t.tryAgainBtn}
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Error */}
          {error && (
            <div style={{ color: "#d90429", marginTop: 20 }}>{error}</div>
          )}
        </div>

          {/* Loading Overlay */}
        {isProcessing && (
          <div className="loading-overlay">
            <div className="spinner" />
          </div>
        )}
      </div>
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);
