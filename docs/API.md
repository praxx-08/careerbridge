# API reference
Base URL: `http://127.0.0.1:5000/api`

First call GET /session. Keep the cookie and send its csrf value as X-CSRF-Token on every POST/PATCH, including login and registration. Login rotates the token; use the new returned value. Bodies are JSON objects. Errors use `{"error":"message"}`.

| Method | Path | Access | Purpose/body |
|---|---|---|---|
| GET | /session | Public | User and CSRF token |
| POST | /register | CSRF | name, email, password (8–128 chars), role (student/recruiter) |
| POST | /login | CSRF | email, password |
| POST | /logout | CSRF | Clear session |
| GET | /jobs | Public | q, location, kind query parameters |
| GET | /jobs/:id | Public | Details, including closed jobs |
| POST | /jobs | Recruiter | title, company, location, kind, salary, skills, description |
| PATCH | /jobs/:id | Owner | status: open/closed |
| POST | /jobs/:id/apply | Student | resume (30–12000 chars), cover_letter (20–4000 chars) |
| POST | /jobs/:id/save | Student | Toggle bookmark; empty object |
| GET | /dashboard | Signed in | Own applications/saved roles or jobs/candidates |
| PATCH | /applications/:id | Owning recruiter | status: Submitted/Shortlisted/Interview/Selected/Rejected |
| POST | /coach | Signed in | mode: review/interview/letter; text (10–12000 chars) |

Employment types: Full-time, Internship, Part-time. Skills are comma-separated text. Salary is display text. All mutations require CSRF.

Codes: 200 success; 201 created; 400 invalid input; 401 authentication; 403 CSRF/role; 404 missing/not-owned record; 409 duplicate; 413 request too large; 503 AI unavailable.
