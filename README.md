# <img src="frontend/src/nivo.png" width="45" align="center" /> Job Agent — NIVO (Strategic Career Assistant)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Node](https://img.shields.io/badge/Node-16%2B-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react&logoColor=white)](https://github.com/facebook/react)
[![Vite](https://img.shields.io/badge/Vite-^5.0.0-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-009688?logo=fastapi&logoColor=white)](https://github.com/tiangolo/fastapi)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-0.22.0-3B82F6?logo=uvicorn&logoColor=white)](https://www.uvicorn.org/)

A compact demo that converts CVs into actionable outputs (analysis, match scoring, tailored cover letters, and interview prep). Built with a clear structure so it’s easy to run locally, inspect behaviour, and adapt for production use.

---

## Table of Contents
- [TL;DR](#tldr)
- [Why "NIVO"?](#why-nivo)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Quick start](#quick-start)
- [API endpoints (summary)](#api-endpoints-summary)
- [Repository prepared for GitHub](#repository-prepared-for-github)
- [Development tips & troubleshooting](#development-tips--troubleshooting)
- [Roadmap](#roadmap)
- [Contributing & license](#contributing--license)

---

## TL;DR

Run the backend and frontend locally; upload/paste a CV, paste a job description, and try Match / Interview / Decide. The system stores session data in-memory and provides a mock mode for offline testing.

## Why "NIVO"?

NIVO mixes approachability with strategy:
- **"Nib" (word choice):** helps you find the right phrasing and ATS-friendly language.
- **Prediction:** estimates likely interview questions and ATS scoring tendencies.
- **Strategic squirrel:** collects and organizes information so you arrive prepared.

<p align="center">
  <img src="frontend/src/nivo.png" width="220" alt="NIVO Mascot" />
</p>

## Features

- **Upload or paste CV:** backend returns a `session_id` for follow-up requests.
- **Decision Center:** Match & Optimize, Interview Prep, Decide.
- **Human-readable outputs:** match score, common terms, suggested CV changes, cover letters, and interview Q&A.
- **Mock Mode:** No OpenAI key required for local testing (optional Real Mode with `OPENAI_API_KEY`).

## Tech stack

- **Backend:** FastAPI + Uvicorn (Python)
- **Frontend:** Vite + React 18
- **Styling:** Modern CSS (Glassmorphism), Heebo font for Hebrew support.
- **Dev/test:** pytest, Vitest/Jest, Playwright/Cypress.

---

## Quick start

### 1. Backend Setup
Choose your preferred mode:

**Option A: Mock Mode (Fast Demo, No API Key)**
```powershell
# Windows
$env:MOCK_MODE = 'true'
uvicorn app:app --reload

# macOS / Linux
export MOCK_MODE=true
uvicorn app:app --reload
```
**Option B: Real Mode (Live OpenAI Intelligence)**

```powershell
# Windows
$env:MOCK_MODE = 'false'
$env:OPENAI_API_KEY = 'your-key-here'
uvicorn app:app --reload

```

### 2. Frontend Setup

In another terminal:

```bash
cd frontend
npm install
npm run dev

```

Visit: [http://localhost:5173](https://www.google.com/search?q=http://localhost:5173) | API: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## API endpoints (summary)

* `POST /upload-cv-file` — multipart upload → `{ session_id, text_preview, length, lang }`
* `POST /analyze-cv` — `{ text?, session_id? }` → analysis
* `POST /match-job` — `{ title, description, session_id? }` → `match_score`, `recommended_changes`, `cover_letter`
* `POST /simulate-interview` — form `title` (or `Role||session_id`) → `questions`, `advice`
* `POST /decide` — `{ session_id }` → `{ action: 'prep_interview'|'improve_cv', match_score }`
* `GET /health` — health and mock-mode flag

---

## Repository prepared for GitHub

* **.gitignore** — ignores virtual environments, node_modules, build artifacts, logs, and secrets.
* **.gitattributes** — normalizes line endings for cross-platform contribution.
* **LICENSE** — MIT license.
* **.github/workflows/ci.yml** — CI to install Python and Node deps and run builds.

---

## Development tips & troubleshooting

* **Mock Mode:** Set `MOCK_MODE=true` to run fully offline.
* **Ports:** Frontend 5173, backend 8000. Ensure your firewall allows these ports.
* **Security & Privacy:** Session data is stored in memory (or Redis if you configure `REDIS_URL`) and not persisted to disk by default.

## Testing & local CI

We added a basic test suite (pytest) and a GitHub Actions workflow that runs backend tests on PRs.

Run the backend tests locally:

```powershell
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
```

Notes:
- The backend tests cover utilities, the OpenAI service wrapper (mocked), prompting helpers, session store, upload size checks and rate limiting.
- CI is configured in `.github/workflows/ci.yml` to run the backend tests automatically on pushes/PRs.

## Configuration (important env vars)

Key environment variables (also included in `.env.example`):

- `MOCK_MODE` (true|false) — prefer `true` for offline testing.
- `OPENAI_API_KEY` — your OpenAI API key (required when `MOCK_MODE=false`).
- `OPENAI_MODEL` — model id to use (default: `gpt-4o-mini`).
- `DECIDE_THRESHOLD` — numeric threshold for `decide()` action (default: `75`).
- `MAX_UPLOAD_SIZE_BYTES` — max upload size for CV files (default: 5MB).
- `RATE_LIMIT_DEFAULT` — default rate limit string (e.g., `60/minute`).
- `ALLOWED_ORIGINS` — CORS origins allowed (configured via `config`).
- `REDIS_URL` — optional Redis URL for session persistence (if not set, an in-memory fallback is used).

These make the app predictable and safer for local development and for production deployments.

---

## Minimal file layout

```
job-agent-nivo/
├── backend/
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   ├── src/main.jsx
│   ├── index.css
│   └── nivo.png
└── README.md

```

---

## Roadmap & ideas

* Add robust PDF and `docx` extraction with retries and chunking.
* Add tokenization and batching logic to avoid token-overflow.
* Extract a shared API client (`frontend/src/api.js`) for cleaner fetch logic.
* Componentize the frontend into `Uploader` and `ResultsPanel`.
* Add backend unit tests (`pytest`) and E2E tests.

---

## Contributing & License

* **Contributions:** Open an issue or PR for feedback and improvements.
* **License:** MIT (see `LICENSE`).

---

<p align="center">
Developed with focus by the NIVO Strategy Team.
</p>
