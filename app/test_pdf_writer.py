from pathlib import Path
import re

from app.document.reader import read_docx
from app.document.pdf_writer import create_cover_letter_pdf

from app.agents.resume_agent import analyze_resume
from app.agents.job_agent import analyze_job
from app.agents.matching_agent import match_candidate_to_job
from app.agents.writer_agent import write_cover_letter
from app.agents.reviewer_agent import review_cover_letter


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
    raise RuntimeError(
        "Multiple job descriptions found. "
        "Keep only one for this test."
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

match = match_candidate_to_job(
    candidate,
    job,
)


# --------------------------------------------------
# Writer Agent
# --------------------------------------------------

print("Running Cover Letter Writer...")

draft = write_cover_letter(
    candidate,
    job,
    match,
)


# --------------------------------------------------
# Reviewer Agent
# --------------------------------------------------

print("Running Reviewer Agent...")

review = review_cover_letter(
    candidate,
    job,
    match,
    draft,
)


# --------------------------------------------------
# Use reviewed letter
# --------------------------------------------------

final_letter = review.revised_cover_letter


# --------------------------------------------------
# Create output filename
# --------------------------------------------------

safe_candidate_name = re.sub(r"[^A-Za-z0-9]+", "", candidate.name)
safe_company_name = re.sub(r"[^A-Za-z0-9]+", "", job.company)

output_file = (
    Path("CoverLetters")
    / f"{safe_candidate_name}-CoverLetter-{safe_company_name}.pdf"
)


# --------------------------------------------------
# Generate PDF
# --------------------------------------------------

print()
print("Generating PDF...")

create_cover_letter_pdf(
    output_path=output_file,
    candidate=candidate,
    job=job,
    cover_letter=final_letter,
)


# --------------------------------------------------
# Result
# --------------------------------------------------

print()
print("=" * 80)
print("PDF CREATED SUCCESSFULLY")
print("=" * 80)

print(f"File: {output_file}")
print(f"Approved by Reviewer: {review.approved}")