# Upload to GitHub and submit
1. Download and extract `CareerBridge-Project.zip` on your laptop.
2. Run the project using README.md. Fill in SUBMISSION.md.
3. Sign in at https://github.com and create a repository named `careerbridge`.
4. Use Public if your evaluator needs access without an invitation; otherwise invite them to a Private repository.
5. Select **uploading an existing file** or **Add file → Upload files**.
6. Upload the files and folders *inside* `careerbridge`. The repository root should show README.md, app.py, schema.sql, static, docs, and tests.
7. Include `.gitignore` and `.env.example`. Enable hidden-file visibility if needed. Never upload `.env`, `.venv`, `instance`, caches, or database files. Browser uploads do not automatically enforce `.gitignore`.
8. Commit with message `Initial CareerBridge project`.
9. Open the repository and verify its README and folders.
10. Submit `https://github.com/YOUR_USERNAME/careerbridge` to college.

Do not upload only the ZIP: the evaluator should be able to browse source files.

## Git command-line alternative
Create an empty repository first, then run inside the extracted project folder:
```bash
git init
git add .
git status
# Confirm .env, .venv, instance and *.db are NOT staged.
git commit -m "Initial CareerBridge project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/careerbridge.git
git push -u origin main
```
Replace YOUR_USERNAME. Git may ask for your author identity and authentication. Never store access tokens in source files.

## Repository versus running website
A repository URL shows the code; it does not run Python. GitHub Pages serves static files and cannot execute this Flask backend. The evaluator can download and run the project. A live URL needs a Python-capable host, persistent database storage, and the hardening described in README.

Official reference: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
