# CareerBridge — College Placement & Career Portal

An independently implemented full-stack job portal inspired by CareerConnect. Students explore opportunities, save roles, apply, and track progress. Recruiters publish jobs and manage candidates.

**Stack:** Python · Flask · SQLite · HTML · CSS · JavaScript

## Features
- Student and recruiter registration/sign-in with password hashing.
- Job search by title, skills, company, location, and employment type.
- Job details, bookmarks, resume-text applications, duplicate prevention.
- Student dashboard with application status.
- Recruiter dashboard with job publishing, closing/reopening roles, and candidate review.
- Resume guidance, interview practice, and cover letter drafting.
- Optional NVIDIA AI with clearly labelled generic offline guidance without a key.
- Responsive UI, validation, error messages, CSRF protection, and ownership checks.
- Six fictional demo vacancies, two accounts, and automated integration tests.

## Run on Windows
Install Python 3.11 or later. Extract the project and open a terminal inside this folder.

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
.venv\Scripts\python -c "import secrets; print(secrets.token_hex(32))"
```
Paste the generated value after `SECRET_KEY=` in `.env`. Then:

```powershell
.venv\Scripts\python -m flask --app app:create_app seed
.venv\Scripts\python app.py
```
Open **http://127.0.0.1:5000**. Keep the terminal running; Ctrl+C stops it.

## Run on macOS / Linux
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
.venv/bin/python -c "import secrets; print(secrets.token_hex(32))"
# Paste the generated value into SECRET_KEY in .env
.venv/bin/python -m flask --app app:create_app seed
.venv/bin/python app.py
```
Do not open `static/index.html` directly or use Live Server. Flask serves both UI and API from the same address. The database `instance/careerbridge.db` is created automatically and persists after restarting.

## Demo accounts
| Role | Email | Password |
|---|---|---|
| Student | student@demo.test | DemoPass123! |
| Recruiter | recruiter@demo.test | DemoPass123! |

The optional seed command is repeatable. These public accounts are for local demonstrations. All seeded companies and jobs are fictional. You can register your own accounts too.

## Five-minute demo
1. Search for Python and Remote; view the internship.
2. Sign in as the student, save a role, and apply with sample resume text.
3. View the submitted application in Dashboard.
4. Sign out and sign in as the recruiter. Read the application and change its status to Interview.
5. Post a new role or close/reopen an existing one.
6. Sign in as the student again to show the updated status.
7. Demonstrate Career coach, explaining whether it is in offline or AI mode.

## Optional NVIDIA AI
Set `NVIDIA_API_KEY` and an exact `NVIDIA_MODEL` identifier supported by your account in `.env`, then restart. The backend calls NVIDIA's OpenAI-compatible chat completions endpoint; the key is never sent to the browser. The live integration has not been tested with real credentials.

Without both values, the coach returns a **generic template, not personalized AI analysis**. With AI enabled, submitted context is sent to NVIDIA. Use fictional information for the demo. Provider errors show a friendly retry message. This is a single-request toolkit, not a conversational assistant with history.

## Tests
Windows: `.venv\Scripts\python -m pytest -q`  
macOS/Linux: `.venv/bin/python -m pytest -q`

Tests use isolated temporary databases. See [validation results](docs/TEST_RESULTS.md).

## Files
| File | Purpose |
|---|---|
| app.py | Flask API, authentication, validation, seed command |
| schema.sql | Relational schema and constraints |
| requirements.txt | Dependencies |
| .env.example / .gitignore | Configuration template and secret/runtime exclusions |
| static/index.html | Application shell |
| static/style.css | Responsive design |
| static/app.js | Views and API interactions |
| tests/test_app.py | Integration tests |
| docs/PROJECT_REPORT.md | Architecture, data model, viva notes |
| docs/API.md | API reference |
| docs/GITHUB_UPLOAD.md | Upload and submission instructions |
| SUBMISSION.md | Your college details template |
| ATTRIBUTION.md | Concept reference and implementation differences |

## Submit to college
Follow [GitHub upload instructions](docs/GITHUB_UPLOAD.md). Upload the extracted source files, not just the ZIP. Fill in [SUBMISSION.md](SUBMISSION.md), review the implementation, and record your own contributions.

GitHub hosts your repository. GitHub Pages cannot execute this Python backend. If college requests a repository URL, submit that URL; a live app needs a separate Python-capable host with persistent storage.

## Scope
This is a local learning MVP. It has no password reset, email verification, recruiter approval, file uploads, pagination, email alerts, admin console, audit log, application withdrawal, or rate limiter. Recruiter roles are self-selected. Resume content is pasted text stored in SQLite.

Before public use: remove demo accounts; add rate limiting, verification, privacy/retention controls, backups and monitoring; use a production WSGI server, HTTPS, persistent storage, a stable random secret, and `COOKIE_SECURE=true`. The built-in server is for local development only.

## Attribution
Concept reference: [mxstafa520/CareerConnect](https://github.com/mxstafa520/CareerConnect).

This package's code, UI, schema, and documentation were independently written with AI assistance. No source files, secrets, or database dumps were copied from the reference. Follow your college's AI-assistance and attribution policies.
