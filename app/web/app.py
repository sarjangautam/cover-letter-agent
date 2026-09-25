import sys
import tempfile
import zipfile

from io import BytesIO
from pathlib import Path

import streamlit as st


# =========================================================
# Fix Python import path
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIRECTORY = str(Path(__file__).resolve().parent)

sys.path = [
    path
    for path in sys.path
    if path != SCRIPT_DIRECTORY
]

sys.path.insert(
    0,
    str(PROJECT_ROOT),
)


from app.services.cover_letter_service import (
    generate_cover_letters,
)


# =========================================================
# Page configuration
# =========================================================

st.set_page_config(
    page_title="Cover Letter Generator",
    page_icon="✉️",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={},
)


# =========================================================
# Custom CSS
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #f4f5f7;
        color: #111827;
    }

    header[data-testid="stHeader"] {
        display: none;
    }

    .stMainBlockContainer {
        padding-top: 0 !important;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    h1 {
        font-size: clamp(2rem, 3.5vw, 3.6rem) !important;
        letter-spacing: -0.06em;
        margin: 0 !important;
        color: #0f172a !important;
        line-height: 0.95 !important;
    }

    h2, h3, .stSubheader {
        letter-spacing: -0.02em;
        color: #0f172a !important;
    }

    .hero-wrap {
        display: flex;
        align-items: center;
        gap: 1.2rem;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }

    .hero-icon {
        width: 72px;
        height: 72px;
        border-radius: 22px;
        background: linear-gradient(135deg, #e9d5ff, #ddd6fe);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 12px 24px rgba(124, 58, 237, 0.12);
        font-size: 2.2rem;
    }

    .hero-subtitle {
        font-size: clamp(1.15rem, 2vw, 1.9rem);
        color: #374151;
        margin: 0 0 1.5rem 0;
        line-height: 1.4;
    }

    .section-shell {
        background: rgba(255,255,255,0.7);
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.04);
        margin-bottom: 1.5rem;
    }

    [data-testid="stFileUploaderDropzone"],
    [data-testid="stBaseButton-secondary"],
    [data-testid="stBaseButton-primary"],
    [data-testid="stSelectbox"] {
        border-radius: 12px;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: rgba(255, 255, 255, 0.9);
        border: 1px dashed #cbd5e1;
        min-height: 90px;
        color: #111827 !important;
    }

    [data-testid="stFileUploaderDropzone"] * {
        color: #111827 !important;
    }

    [data-testid="stFileUploaderDropzone"] button,
    [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] {
        color: #0f172a !important;
        font-weight: 600 !important;
        background: #f8fafc !important;
        border: 1px solid #cbd5e1 !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #111827 !important;
        opacity: 1 !important;
    }

    [data-testid="stFileUploaderLabel"] {
        color: #111827 !important;
        font-weight: 600 !important;
    }

    [data-testid="stAppViewContainer"] main,
    [data-testid="stAppViewContainer"] main p,
    [data-testid="stAppViewContainer"] main li,
    [data-testid="stAppViewContainer"] main label,
    [data-testid="stAppViewContainer"] main small,
    [data-testid="stMarkdownContainer"] *,
    [data-testid="stCaptionContainer"] *,
    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricValue"] * {
        color: #111827 !important;
    }

    [data-testid="stMarkdownContainer"] {
        color: #111827 !important;
    }

    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-testid="stDownloadButton"] button,
    [data-testid="stFormSubmitButton"] button,
    [data-testid="stMetric"],
    [data-testid="stExpander"] {
        background: #ffffff !important;
        color: #111827 !important;
        border-color: #cbd5e1 !important;
    }

    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        min-height: 2.75rem;
        border: 1px solid #94a3b8 !important;
    }

    [data-testid="stDownloadButton"] button {
        min-height: 2.75rem;
        font-weight: 700 !important;
    }

    [data-testid="stFormSubmitButton"] button {
        background: #4338ca !important;
        border-color: #4338ca !important;
        color: #ffffff !important;
    }

    [data-testid="stFormSubmitButton"] button p {
        color: #ffffff !important;
    }

    [data-testid="stDownloadButton"] button p,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary * {
        color: #111827 !important;
    }

    [data-testid="stMetric"] {
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
    }

    [data-testid="stProgress"] > div > div {
        background: #4338ca !important;
    }

    [data-testid="stAlert"] {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
    }

    div[data-testid="stFileUploader"] > label,
    div[data-testid="stSelectbox"] label {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }

    div[data-testid="stSelectbox"] > div {
        background: #ffffff !important;
        border: 1px solid #94a3b8 !important;
        color: #111827 !important;
    }

    div[data-testid="stSelectbox"] [data-baseweb="select"] * {
        color: #111827 !important;
    }

    div[data-testid="stForm"] h2,
    div[data-testid="stForm"] h3,
    div[data-testid="stForm"] [data-testid="stSubheader"] {
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    div[data-testid="stForm"] [data-testid="stCaptionContainer"],
    div[data-testid="stForm"] [data-testid="stCaptionContainer"] * {
        color: #374151 !important;
        opacity: 1 !important;
    }

    [role="listbox"],
    [role="option"] {
        background: #ffffff !important;
        color: #111827 !important;
    }

    [role="option"] * {
        color: #111827 !important;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #dfe7f3;
        border-radius: 14px;
        background: #ffffff;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    }

    div[data-testid="stExpanderDetails"] {
        background: #ffffff;
        color: #111827 !important;
        padding: 0.9rem 1rem 1rem 1rem;
    }

    div[data-testid="stExpanderDetails"] * {
        color: #111827 !important;
    }

    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown strong,
    .stMarkdown em,
    .stMarkdown div,
    .stMarkdown span {
        color: #111827 !important;
    }

    .stAlert,
    .stSuccess,
    .stWarning,
    .stInfo,
    .stError {
        color: #111827 !important;
    }

    .stAlert > div,
    .stSuccess > div,
    .stWarning > div,
    .stInfo > div,
    .stError > div {
        color: #111827 !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
    }

    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 0.8rem 1rem;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
    }

    .result-shell {
        background: rgba(255,255,255,0.85);
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 1.3rem 1.2rem 1rem 1.2rem;
        margin: 1rem 0 1.5rem 0;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
    }

    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 0.75rem;
        margin-bottom: 0.8rem;
    }

    .result-index {
        color: #6366f1;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
    }

    .result-role {
        margin: 0;
        font-size: 1.5rem;
        line-height: 1.2;
        color: #111827;
    }

    .result-company-badge {
        background: #eef2ff;
        color: #3730a3;
        border-radius: 999px;
        padding: 0.4rem 0.75rem;
        font-size: 0.76rem;
        font-weight: 700;
        border: 1px solid #c7d2fe;
        white-space: nowrap;
    }

    .preview-paper {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.4rem 1.5rem;
        color: #111827;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
        line-height: 1.7;
    }

    .preview-paper p {
        margin: 0.6rem 0;
        color: #111827 !important;
    }

    .preview-paper strong {
        color: #111827 !important;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        border: none;
        transition: 0.2s ease;
    }

    div[data-testid="stFormSubmitButton"] > button {
        min-height: 3.25rem;
        background: #4338ca !important;
        color: #ffffff !important;
        font-size: 1.05rem;
        font-weight: 700;
        box-shadow: 0 8px 18px rgba(67, 56, 202, 0.22);
    }

    div[data-testid="stFormSubmitButton"] > button p {
        color: #ffffff !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.15);
    }

    .stDownloadButton > button {
        border-radius: 10px;
        border: 1px solid #dbe3f0;
        background: #ffffff;
    }

    div[data-testid="stForm"] {
        background: rgba(255,255,255,0.7);
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.04);
    }

    .footer {
        text-align: center;
        color: #667085;
        margin-top: 40px;
        padding-bottom: 20px;
        font-size: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Header
# =========================================================

st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-icon">✉️</div>
        <h1>Cover Letter Generator</h1>
    </div>
    <p class="hero-subtitle">
        Create tailored, professional cover letters from your resume and job descriptions.
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()

with st.form("cover_letter_form"):
    # =========================================================
    # Resume upload
    # =========================================================

    st.subheader("1. Upload your resume")

    resume_file = st.file_uploader(
        "Upload your resume",
        type=["docx"],
        help="Upload your current resume in Microsoft Word format.",
    )


    # =========================================================
    # Job descriptions
    # =========================================================

    st.subheader("2. Upload job descriptions")

    job_files = st.file_uploader(
        "Upload one or more job descriptions",
        type=["docx"],
        accept_multiple_files=True,
        help="You can upload multiple job descriptions at once.",
    )


    # =========================================================
    # Writing style
    # =========================================================

    st.subheader("3. Choose writing style")

    writing_style = st.selectbox(
        "Cover letter style",
        [
            "Professional",
            "Warm & Conversational",
            "Concise & Direct",
        ],
    )

    style_descriptions = {
        "Professional": (
            "Polished, clear and business-focused."
        ),
        "Warm & Conversational": (
            "Personable, approachable and professional."
        ),
        "Concise & Direct": (
            "Focused, straightforward and efficient."
        ),
    }

    st.caption(
        style_descriptions[writing_style]
    )


    output_format = st.selectbox(
        "Download format",
        ["PDF", "DOCX"],
        help="Choose the file format for generated cover letters.",
    )


    # =========================================================
    # Generate button
    # =========================================================

    st.divider()

    generate_button = st.form_submit_button(
        "🚀 Generate Cover Letters",
        type="primary",
        use_container_width=True,
    )


# =========================================================
# Generation
# =========================================================

if generate_button:

    # -----------------------------------------------------
    # Validate uploads
    # -----------------------------------------------------

    if resume_file is None:

        st.error(
            "Please upload your resume before generating cover letters."
        )

        st.stop()

    if not job_files:

        st.error(
            "Please upload at least one job description."
        )

        st.stop()


    # -----------------------------------------------------
    # Temporary working directory
    # -----------------------------------------------------

    with tempfile.TemporaryDirectory() as temp_directory:

        temp_path = Path(temp_directory)

        resume_path = (
            temp_path
            / resume_file.name
        )

        resume_path.write_bytes(
            resume_file.getbuffer()
        )


        # -------------------------------------------------
        # Save job descriptions
        # -------------------------------------------------

        job_paths = []

        for job_file in job_files:

            job_path = (
                temp_path
                / job_file.name
            )

            job_path.write_bytes(
                job_file.getbuffer()
            )

            job_paths.append(
                job_path
            )


        # -------------------------------------------------
        # Output folder
        # -------------------------------------------------

        output_folder = (
            temp_path
            / "CoverLetters"
        )

        output_folder.mkdir(
            parents=True,
            exist_ok=True,
        )


        # -------------------------------------------------
        # Progress UI
        # -------------------------------------------------

        st.subheader(
            "Generating applications"
        )

        progress_bar = st.progress(
            0
        )

        progress_status = st.empty()


        def update_progress(
            job_index,
            total_jobs,
            job_name,
            stage,
        ):

            # Resume-level stages
            if job_index == 0:

                progress_status.info(
                    stage
                )

                return


            # Calculate approximate progress
            progress = (
                job_index
                / total_jobs
            )

            progress_bar.progress(
                min(
                    progress,
                    1.0,
                )
            )

            if job_name:

                progress_status.info(
                    f"Job {job_index} of "
                    f"{total_jobs}: "
                    f"{job_name} — "
                    f"{stage}"
                )

            else:

                progress_status.info(
                    stage
                )


        # -------------------------------------------------
        # Generate cover letters
        # -------------------------------------------------

        try:

            generation_result = (
                generate_cover_letters(
                    resume_file=resume_path,
                    job_files=job_paths,
                    output_folder=output_folder,
                    progress_callback=update_progress,
                    writing_style=writing_style,
                    output_format=output_format,
                )
            )

        except Exception as error:

            progress_bar.progress(
                0
            )

            progress_status.empty()

            st.error(
                "An unexpected error occurred "
                "while generating the cover letters."
            )

            st.exception(
                error
            )

            st.stop()


        # -------------------------------------------------
        # Complete progress
        # -------------------------------------------------

        progress_bar.progress(
            1.0
        )

        progress_status.success(
            "All cover letters have been processed."
        )


        # -------------------------------------------------
        # Results
        # -------------------------------------------------

        candidate = generation_result[
            "candidate"
        ]

        results = generation_result[
            "results"
        ]

        total_jobs = generation_result[
            "total"
        ]

        successful = generation_result[
            "successful"
        ]

        failed = generation_result[
            "failed"
        ]

        file_mime = (
            "application/pdf"
            if output_format == "PDF"
            else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )


        # -------------------------------------------------
        # Summary metrics
        # -------------------------------------------------

        st.divider()

        st.subheader(
            "Generation Summary"
        )

        summary_columns = st.columns(
            3
        )

        summary_columns[0].metric(
            "Jobs",
            total_jobs,
        )

        summary_columns[1].metric(
            "Successful",
            successful,
        )

        summary_columns[2].metric(
            "Failed",
            failed,
        )


        st.caption(
            f"Writing style: {writing_style}"
        )


        # =================================================
        # Application results
        # =================================================

        st.divider()

        st.subheader(
            "Applications"
        )


        for index, item in enumerate(
            results,
            start=1,
        ):

            job_file = item[
                "job_file"
            ]

            company = item.get(
                "company"
            )

            role = item.get(
                "role"
            )

            output_file = item.get(
                "output_file"
            )

            cover_letter = item.get(
                "cover_letter"
            )

            error = item.get(
                "error"
            )


            # -------------------------------------------------
            # Application title
            # -------------------------------------------------

            display_role = (
                role
                if role
                else job_file.stem
            )

            display_company = (
                company
                if company
                else "Application"
            )


            st.markdown(
                f"""
                <div class="result-header">
                    <div>
                        <div class="result-index">Application {index}</div>
                        <div class="result-role">{display_role}</div>
                    </div>
                    <div class="result-company-badge">{display_company}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


            # -------------------------------------------------
            # Failed application
            # -------------------------------------------------

            if error:

                st.error(
                    f"Failed to generate this cover letter: "
                    f"{error}"
                )

                continue


            # =================================================
            # Application Summary
            # =================================================

            with st.expander(
                "📋 Application Summary",
                expanded=True,
            ):

                summary_col1, summary_col2 = (
                    st.columns(2)
                )


                with summary_col1:

                    st.caption(
                        "ROLE"
                    )

                    st.markdown(
                        f"<div style='color:#111827; font-weight:600;'>{role}</div>",
                        unsafe_allow_html=True,
                    )


                with summary_col2:

                    st.caption(
                        "COMPANY"
                    )

                    st.markdown(
                        f"<div style='color:#111827; font-weight:600;'>{company}</div>",
                        unsafe_allow_html=True,
                    )


                st.divider()


                st.caption(
                    "WRITING STYLE"
                )

                st.markdown(
                    f"<div style='color:#111827;'>{writing_style}</div>",
                    unsafe_allow_html=True,
                )


                st.caption(
                    "MATCHING OVERVIEW"
                )


                strong_matches = item.get(
                    "strong_matches",
                    [],
                )

                transferable_skills = item.get(
                    "transferable_skills",
                    [],
                )

                development_areas = item.get(
                    "development_areas",
                    [],
                )


                matching_columns = (
                    st.columns(3)
                )


                matching_columns[0].metric(
                    "Strong Matches",
                    len(
                        strong_matches
                    ),
                )


                matching_columns[1].metric(
                    "Transferable Skills",
                    len(
                        transferable_skills
                    ),
                )


                matching_columns[2].metric(
                    "Development Areas",
                    len(
                        development_areas
                    ),
                )


            # =================================================
            # Review scores
            # =================================================

            score_columns = st.columns(
                4
            )


            accuracy_score = item.get(
                "accuracy_score"
            )

            relevance_score = item.get(
                "relevance_score"
            )

            naturalness_score = item.get(
                "naturalness_score"
            )

            professionalism_score = item.get(
                "professionalism_score"
            )


            score_columns[0].metric(
                "Accuracy",
                (
                    f"{accuracy_score}/10"
                    if accuracy_score is not None
                    else "N/A"
                ),
            )


            score_columns[1].metric(
                "Relevance",
                (
                    f"{relevance_score}/10"
                    if relevance_score is not None
                    else "N/A"
                ),
            )


            score_columns[2].metric(
                "Naturalness",
                (
                    f"{naturalness_score}/10"
                    if naturalness_score is not None
                    else "N/A"
                ),
            )


            score_columns[3].metric(
                "Professional",
                (
                    f"{professionalism_score}/10"
                    if professionalism_score is not None
                    else "N/A"
                ),
            )


            # =================================================
            # Review status
            # =================================================

            approved = item.get(
                "approved",
                False,
            )


            if approved:

                st.success(
                    "✓ Cover letter approved by reviewer"
                )

            else:

                st.warning(
                    "⚠ Cover letter generated, "
                    "but reviewer did not approve it."
                )


            # =================================================
            # Matching Analysis
            # =================================================

            with st.expander(
                "🔎 Why this application was tailored",
                expanded=False,
            ):

                strong_matches = item.get(
                    "strong_matches",
                    [],
                )

                transferable_skills = item.get(
                    "transferable_skills",
                    [],
                )

                development_areas = item.get(
                    "development_areas",
                    [],
                )

                recommended_focus = item.get(
                    "recommended_focus",
                    [],
                )

                unsupported_requirements = item.get(
                    "unsupported_requirements",
                    [],
                )


                # ---------------------------------------------
                # Strong Matches
                # ---------------------------------------------

                if strong_matches:

                    st.markdown(
                        "### ✓ Strong Matches"
                    )

                    for match_item in (
                        strong_matches
                    ):

                        st.markdown(
                            f"<div style='color:#111827; margin-bottom:0.35rem;'>✓ {match_item}</div>",
                            unsafe_allow_html=True,
                        )


                # ---------------------------------------------
                # Transferable Skills
                # ---------------------------------------------

                if transferable_skills:

                    st.markdown(
                        "### 🔄 Transferable Skills"
                    )

                    for skill in (
                        transferable_skills
                    ):

                        st.markdown(
                            f"<div style='color:#111827; margin-bottom:0.35rem;'>✓ {skill}</div>",
                            unsafe_allow_html=True,
                        )


                # ---------------------------------------------
                # Development Areas
                # ---------------------------------------------

                if development_areas:

                    st.markdown(
                        "### 📈 Development Areas"
                    )

                    for area in (
                        development_areas
                    ):

                        st.markdown(
                            f"<div style='color:#111827; margin-bottom:0.35rem;'>• {area}</div>",
                            unsafe_allow_html=True,
                        )


                # ---------------------------------------------
                # Recommended Focus
                # ---------------------------------------------

                if recommended_focus:

                    st.markdown(
                        "### 🎯 Recommended Focus"
                    )

                    for focus in (
                        recommended_focus
                    ):

                        st.markdown(
                            f"<div style='color:#111827; margin-bottom:0.35rem;'>✓ {focus}</div>",
                            unsafe_allow_html=True,
                        )


                # ---------------------------------------------
                # Unsupported Requirements
                # ---------------------------------------------

                if unsupported_requirements:

                    st.markdown(
                        "### ℹ️ Requirements Not Directly Supported"
                    )

                    st.caption(
                        "These requirements were identified "
                        "in the job description but were not "
                        "directly supported by the resume."
                    )

                    for requirement in (
                        unsupported_requirements
                    ):

                        st.markdown(
                            f"<div style='color:#111827; margin-bottom:0.35rem;'>• {requirement}</div>",
                            unsafe_allow_html=True,
                        )


                # ---------------------------------------------
                # No matching analysis
                # ---------------------------------------------

                if not any(
                    [
                        strong_matches,
                        transferable_skills,
                        development_areas,
                        recommended_focus,
                        unsupported_requirements,
                    ]
                ):

                    st.info(
                        "No matching analysis is available "
                        "for this application."
                    )


            # =================================================
            # Cover Letter Preview
            # =================================================

            if cover_letter:

                with st.expander(
                    "📄 Preview Cover Letter",
                    expanded=False,
                ):

                    preview_text = (
                        f"**{cover_letter.greeting}**\n\n"
                        f"{cover_letter.opening}\n\n"
                    )

                    for paragraph in cover_letter.body:
                        preview_text += f"{paragraph}\n\n"

                    preview_text += (
                        f"{cover_letter.closing}\n\n"
                        f"{cover_letter.sign_off}\n\n"
                        f"{candidate.name}"
                    )

                    st.markdown(
                        f"<div class='preview-paper'>{preview_text}</div>",
                        unsafe_allow_html=True,
                    )


            # =================================================
            # Download selected format
            # =================================================

            if output_file and output_file.exists():

                document_bytes = (
                    output_file.read_bytes()
                )


                st.download_button(
                    label=f"⬇️ Download {output_format}",
                    data=document_bytes,
                    file_name=output_file.name,
                    mime=file_mime,
                    key=f"download_{output_format.lower()}_{index}",
                    use_container_width=True,
                )


            st.divider()

        # =================================================
        # ZIP download
        # =================================================

        successful_results = [
            item
            for item in results
            if (
                item.get("output_file")
                and item["output_file"].exists()
            )
        ]


        if successful_results:

            zip_buffer = BytesIO()


            with zipfile.ZipFile(
                zip_buffer,
                mode="w",
                compression=zipfile.ZIP_DEFLATED,
            ) as zip_file:

                for item in successful_results:

                    output_file = item[
                        "output_file"
                    ]

                    zip_file.write(
                        output_file,
                        arcname=output_file.name,
                    )


            zip_buffer.seek(0)


            st.subheader(
                "Download All"
            )


            st.download_button(
                label=f"📦 Download All {output_format} Cover Letters",
                data=zip_buffer.getvalue(),
                file_name=(
                    f"CoverLetters-{output_format.lower()}.zip"
                ),
                mime="application/zip",
                use_container_width=True,
            )


        # =================================================
        # Start Again
        # =================================================

        st.divider()


        if st.button(
            "🔄 Start Again",
            use_container_width=True,
        ):

            st.rerun()


# =========================================================
# Footer
# =========================================================

st.markdown(
    """
    <div class="footer">

        Cover Letter Generator<br>
        Tailored applications powered by AI

    </div>
    """,
    unsafe_allow_html=True,
)