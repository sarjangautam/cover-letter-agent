from pathlib import Path
import re

from app.agents.resume_agent import analyze_resume
from app.agents.job_agent import analyze_job
from app.agents.matching_agent import match_candidate_to_job
from app.agents.writer_agent import write_cover_letter
from app.agents.reviewer_agent import review_cover_letter

from app.document.reader import read_docx
from app.document.docx_writer import create_cover_letter_docx
from app.document.pdf_writer import create_cover_letter_pdf


def generate_cover_letters(
    resume_file: Path,
    job_files: list[Path],
    output_folder: Path,
    progress_callback=None,
    writing_style: str = "Professional",
    output_format: str = "PDF",
):
    """
    Generate a tailored PDF cover letter for every job description.

    The resume is analysed once and then reused for every job.

    progress_callback:
        Optional function that receives progress information.
    """

    allowed_formats = {
        "PDF": (".pdf", "Creating PDF..."),
        "DOCX": (".docx", "Creating DOCX..."),
    }

    if output_format not in allowed_formats:
        raise ValueError(
            f"Unsupported output format: {output_format}. "
            f"Choose one of: {', '.join(allowed_formats)}"
        )

    output_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    def report_progress(
        job_index,
        total_jobs,
        job_name,
        stage,
    ):
        if progress_callback:
            progress_callback(
                job_index,
                total_jobs,
                job_name,
                stage,
            )

    # ---------------------------------------------------------
    # Analyse resume once
    # ---------------------------------------------------------

    report_progress(
        0,
        len(job_files),
        "",
        "Analysing resume...",
    )

    resume_text = read_docx(resume_file)

    candidate = analyze_resume(resume_text)

    report_progress(
        0,
        len(job_files),
        "",
        "Resume analysed successfully.",
    )

    # ---------------------------------------------------------
    # Process jobs
    # ---------------------------------------------------------

    results = []

    successful = 0
    failed = 0

    for index, job_file in enumerate(
        job_files,
        start=1,
    ):

        job_name = job_file.name

        try:

            # ---------------------------------------------
            # Read job description
            # ---------------------------------------------

            report_progress(
                index,
                len(job_files),
                job_name,
                "Reading job description...",
            )

            job_text = read_docx(job_file)

            # ---------------------------------------------
            # Analyse job
            # ---------------------------------------------

            report_progress(
                index,
                len(job_files),
                job_name,
                "Analysing job description...",
            )

            job = analyze_job(job_text)

            # ---------------------------------------------
            # Match candidate
            # ---------------------------------------------

            report_progress(
                index,
                len(job_files),
                job_name,
                "Matching your experience to the role...",
            )

            match = match_candidate_to_job(
                candidate,
                job,
            )

            # ---------------------------------------------
            # Write cover letter
            # ---------------------------------------------

            report_progress(
                index,
                len(job_files),
                job_name,
                "Writing tailored cover letter...",
            )

            draft = write_cover_letter(
                candidate,
                job,
                match,
                writing_style=writing_style,
            )

            # ---------------------------------------------
            # Review cover letter
            # ---------------------------------------------

            report_progress(
                index,
                len(job_files),
                job_name,
                "Reviewing cover letter...",
            )

            review = review_cover_letter(
                candidate,
                job,
                match,
                draft,
                writing_style=writing_style,
            )

            # ---------------------------------------------
            # Final letter
            # ---------------------------------------------

            final_letter = review.revised_cover_letter

            # ---------------------------------------------
            # Generate selected document format
            # ---------------------------------------------

            report_progress(
                index,
                len(job_files),
                job_name,
                allowed_formats[output_format][1],
            )

            safe_candidate_name = re.sub(
                r"[^A-Za-z0-9]+",
                "",
                candidate.name,
            )

            safe_company_name = re.sub(
                r"[^A-Za-z0-9]+",
                "",
                job.company,
            )

            output_file = (
                output_folder
                / f"{safe_candidate_name}-CoverLetter-"
                f"{safe_company_name}{allowed_formats[output_format][0]}"
            )

            if output_format == "PDF":
                create_cover_letter_pdf(
                    output_path=output_file,
                    candidate=candidate,
                    job=job,
                    cover_letter=final_letter,
                )
            else:
                create_cover_letter_docx(
                    output_path=output_file,
                    candidate=candidate,
                    job=job,
                    cover_letter=final_letter,
                )

            # ---------------------------------------------
            # Save result
            # ---------------------------------------------

            result = {
                "job_file": job_file,
                "output_file": output_file,
                "company": job.company,
                "role": job.role,
                "cover_letter": final_letter,

                # Matching analysis
                "strong_matches": match.strong_matches,
                "transferable_skills": match.transferable_skills,
                "development_areas": match.development_areas,
                "recommended_focus": match.recommended_focus,
                "unsupported_requirements": (
                    match.unsupported_requirements
                ),

                # Reviewer results
                "approved": review.approved,
                "accuracy_score": review.accuracy_score,
                "relevance_score": review.relevance_score,
                "naturalness_score": review.naturalness_score,
                "professionalism_score": (
                    review.professionalism_score
                ),

                "error": None,
            }

            results.append(result)

            successful += 1

            # ---------------------------------------------
            # Job completed
            # ---------------------------------------------

            report_progress(
                index,
                len(job_files),
                job_name,
                "Completed successfully.",
            )

        except Exception as error:

            failed += 1

            result = {
                "job_file": job_file,
                "output_file": None,
                "company": None,
                "role": None,
                "cover_letter": None,

                # Matching analysis
                "strong_matches": [],
                "transferable_skills": [],
                "development_areas": [],
                "recommended_focus": [],
                "unsupported_requirements": [],

                # Reviewer results
                "approved": False,
                "accuracy_score": None,
                "relevance_score": None,
                "naturalness_score": None,
                "professionalism_score": None,

                "error": str(error),
            }

            results.append(result)

            report_progress(
                index,
                len(job_files),
                job_name,
                f"Failed: {error}",
            )

    return {
        "candidate": candidate,
        "results": results,
        "total": len(job_files),
        "successful": successful,
        "failed": failed,
    }