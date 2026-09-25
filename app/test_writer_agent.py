from pathlib import Path

from app.document.reader import read_docx
from app.agents.resume_agent import analyze_resume
from app.agents.job_agent import analyze_job
from app.agents.matching_agent import match_candidate_to_job
from app.agents.writer_agent import write_cover_letter


# --------------------------------------------------
# Find resume
# --------------------------------------------------

resume_files = list(Path("Resume").glob("*.docx"))

if not resume_files:
    raise RuntimeError("No resume found.")

if len(resume_files) > 1:
    raise RuntimeError("Multiple resumes found.")

resume_file = resume_files[0]


# --------------------------------------------------
# Find job
# --------------------------------------------------

job_files = list(Path("NewJobs").glob("*.docx"))

if not job_files:
    raise RuntimeError("No job description found.")

if len(job_files) > 1:
    raise RuntimeError("Multiple job descriptions found.")

job_file = job_files[0]


# --------------------------------------------------
# Read documents
# --------------------------------------------------

print(f"Reading resume: {resume_file.name}")
resume_text = read_docx(resume_file)

print(f"Reading job description: {job_file.name}")
job_text = read_docx(job_file)


# --------------------------------------------------
# Resume Agent
# --------------------------------------------------

print()
print("Running Resume Agent...")

candidate = analyze_resume(resume_text)


# --------------------------------------------------
# Job Agent
# --------------------------------------------------

print("Running Job Agent...")

job = analyze_job(job_text)


# --------------------------------------------------
# Matching Agent
# --------------------------------------------------

print("Running Matching Agent...")

match = match_candidate_to_job(candidate, job)


# --------------------------------------------------
# Writer Agent
# --------------------------------------------------

print("Running Cover Letter Writer...")

cover_letter = write_cover_letter(
    candidate,
    job,
    match,
)


# --------------------------------------------------
# Display
# --------------------------------------------------

print()
print("=" * 80)
print("GENERATED COVER LETTER")
print("=" * 80)
print()

print(cover_letter.greeting)
print()

print(cover_letter.opening)
print()

for paragraph in cover_letter.body:
    print(paragraph)
    print()

print(cover_letter.closing)
print()

print(cover_letter.sign_off)
print(candidate.name)