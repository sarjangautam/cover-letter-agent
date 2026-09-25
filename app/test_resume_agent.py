from pathlib import Path

from app.document.reader import read_docx
from app.agents.resume_agent import analyze_resume


resume_folder = Path("Resume")

resume_files = list(resume_folder.glob("*.docx"))

if not resume_files:
    raise RuntimeError("No resume found in the Resume folder.")

if len(resume_files) > 1:
    raise RuntimeError(
        "Multiple resume files found. "
        "Please keep only one resume for now."
    )

resume_file = resume_files[0]

print(f"Reading resume: {resume_file.name}")
print()

resume_text = read_docx(resume_file)

print("Sending resume to Resume Agent...")
print()

candidate = analyze_resume(resume_text)

print("=" * 80)
print("STRUCTURED CANDIDATE PROFILE")
print("=" * 80)

print(candidate.model_dump_json(indent=2))