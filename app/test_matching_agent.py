from pathlib import Path

from app.document.reader import read_docx
from app.agents.resume_agent import analyze_resume
from app.agents.job_agent import analyze_job
from app.agents.matching_agent import match_candidate_to_job


# --------------------------------------------------
# Find resume
# --------------------------------------------------

resume_folder = Path("Resume")

resume_files = list(resume_folder.glob("*.docx"))

if not resume_files:
    raise RuntimeError(
        "No resume found in the Resume folder."
    )

if len(resume_files) > 1:
    raise RuntimeError(
        "Multiple resume files found. "
        "Please keep only one resume for now."
    )

resume_file = resume_files[0]


# --------------------------------------------------
# Find job
# --------------------------------------------------

job_folder = Path("NewJobs")

job_files = list(job_folder.glob("*.docx"))

if not job_files:
    raise RuntimeError(
        "No job description found in the NewJobs folder."
    )

if len(job_files) > 1:
    raise RuntimeError(
        "Multiple job descriptions found. "
        "Please keep only one job description for now."
    )

job_file = job_files[0]


# --------------------------------------------------
# Read documents
# --------------------------------------------------

print(f"Reading resume: {resume_file.name}")
resume_text = read_docx(resume_file)

print(f"Reading job description: {job_file.name}")
job_text = read_docx(job_file)


# --------------------------------------------------
# Analyze resume
# --------------------------------------------------

print()
print("Running Resume Agent...")

candidate = analyze_resume(resume_text)


# --------------------------------------------------
# Analyze job
# --------------------------------------------------

print("Running Job Agent...")

job = analyze_job(job_text)


# --------------------------------------------------
# Match candidate to job
# --------------------------------------------------

print("Running Matching Agent...")

match = match_candidate_to_job(candidate, job)


# --------------------------------------------------
# Display result
# --------------------------------------------------

print()
print("=" * 80)
print("CANDIDATE → JOB MATCH")
print("=" * 80)

print(match.model_dump_json(indent=2))