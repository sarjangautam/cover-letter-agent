from pathlib import Path

from app.services.cover_letter_service import generate_cover_letters


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESUME_FOLDER = PROJECT_ROOT / "Resume"
JOBS_FOLDER = PROJECT_ROOT / "NewJobs"
OUTPUT_FOLDER = PROJECT_ROOT / "CoverLetters"


def find_resume() -> Path:

    resume_files = list(
        RESUME_FOLDER.glob("*.docx")
    )

    if not resume_files:
        raise FileNotFoundError(
            f"No DOCX resume found in {RESUME_FOLDER}"
        )

    if len(resume_files) > 1:

        names = "\n".join(
            f"  - {file.name}"
            for file in resume_files
        )

        raise RuntimeError(
            "Multiple resume files found. "
            "Please keep only one resume:\n"
            f"{names}"
        )

    return resume_files[0]


def find_jobs() -> list[Path]:

    job_files = sorted(
        JOBS_FOLDER.glob("*.docx")
    )

    if not job_files:
        raise FileNotFoundError(
            f"No DOCX job descriptions found in {JOBS_FOLDER}"
        )

    return job_files


def main():

    print("=" * 80)
    print("AI COVER LETTER GENERATOR")
    print("=" * 80)

    # --------------------------------------------------------------
    # Find resume
    # --------------------------------------------------------------

    resume_file = find_resume()

    print()
    print(f"Resume: {resume_file.name}")

    # --------------------------------------------------------------
    # Find jobs
    # --------------------------------------------------------------

    job_files = find_jobs()

    print(
        f"Found {len(job_files)} job description(s)."
    )

    # --------------------------------------------------------------
    # Generate cover letters
    # --------------------------------------------------------------

    result = generate_cover_letters(
        resume_file=resume_file,
        job_files=job_files,
        output_folder=OUTPUT_FOLDER,
    )

    # --------------------------------------------------------------
    # Summary
    # --------------------------------------------------------------

    print()
    print("=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)

    print(f"Total jobs: {result['total']}")
    print(f"Successful: {result['successful']}")
    print(f"Failed: {result['failed']}")

    print()
    print(f"Output folder: {OUTPUT_FOLDER}")

    # --------------------------------------------------------------
    # Show results
    # --------------------------------------------------------------

    for item in result["results"]:

        print()

        if item["error"]:

            print(
                f"FAILED: {item['job_file'].name}"
            )

            print(
                f"Error: {item['error']}"
            )

        else:

            print(
                f"SUCCESS: {item['job_file'].name}"
            )

            print(
                f"PDF: {item['output_file'].name}"
            )

            print(
                f"Approved: {item['approved']}"
            )


if __name__ == "__main__":
    main()