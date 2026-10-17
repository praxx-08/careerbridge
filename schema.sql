PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
 password_hash TEXT NOT NULL, role TEXT NOT NULL CHECK(role IN ('student','recruiter'))
);
CREATE TABLE IF NOT EXISTS jobs (
 id INTEGER PRIMARY KEY, recruiter_id INTEGER NOT NULL REFERENCES users(id),
 title TEXT NOT NULL, company TEXT NOT NULL, location TEXT NOT NULL,
 kind TEXT NOT NULL, salary TEXT NOT NULL, skills TEXT NOT NULL,
 description TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','closed')),
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS applications (
 id INTEGER PRIMARY KEY, job_id INTEGER NOT NULL REFERENCES jobs(id),
 student_id INTEGER NOT NULL REFERENCES users(id), resume TEXT NOT NULL,
 cover_letter TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Submitted'
 CHECK(status IN ('Submitted','Shortlisted','Interview','Selected','Rejected')),
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, UNIQUE(job_id,student_id)
);
CREATE TABLE IF NOT EXISTS saved_jobs (
 student_id INTEGER NOT NULL REFERENCES users(id), job_id INTEGER NOT NULL REFERENCES jobs(id),
 PRIMARY KEY(student_id,job_id)
);
