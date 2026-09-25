from pathlib import Path

from app.document.reader import read_docx
from app.agents.job_agent import analyze_job


job_folder = Path("NewJobs")

job_files = list(job_folder.glob("*.docx"))

if not job_files:
    raise RuntimeError(
        "No job description DOCX found in the NewJobs folder."
    )

if len(job_files) > 1:
    print("Multiple job descriptions found:")

    for file in job_files:
        print(f"  - {file.name}")

    print("\nFor this test, please keep only one job description.")
    exit()


job_file = job_files[0]

print(f"Reading job description: {job_file.name}")
print()

job_text = read_docx(job_file)

print("Sending job description to Job Agent...")
print()

job = analyze_job(job_text)

print("=" * 80)
print("STRUCTURED JOB ANALYSIS")
print("=" * 80)

print(job.model_dump_json(indent=2))