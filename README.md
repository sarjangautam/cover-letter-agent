# Cover Letter Agent

Cover Letter Agent is a Python and Streamlit application that uses OpenAI structured responses to create tailored cover letters from a candidate resume and one or more job descriptions.

The application:

- Extracts structured candidate information from a resume.
- Extracts requirements, responsibilities, priorities, and values from each job description.
- Compares the candidate with each role using direct matches, transferable skills, and development areas.
- Writes a tailored cover letter in a selected style.
- Reviews the draft for accuracy, relevance, naturalness, professionalism, unsupported claims, and style consistency.
- Exports the reviewed letter as PDF or DOCX.

## How It Works

For every job description, the application runs this pipeline:

1. Read the resume and job description.
2. Analyze the resume into a `CandidateProfile`.
3. Analyze the job into a `JobAnalysis`.
4. Match the candidate with the job into a `CandidateJobMatch`.
5. Write a structured `CoverLetter`.
6. Review and revise the letter into a `ReviewResult`.
7. Export the reviewed letter in the selected format.

The resume is analyzed once per generation run. Each job is processed independently, so a failed job is reported while other jobs continue. A failure to analyze the resume stops the run.

## Streamlit Application

Start the web interface from the project root:

```powershell
streamlit run app/web/app.py
```

The interface allows you to:

1. Upload exactly one resume.
2. Upload one or more job descriptions.
3. Select a writing style:
   - `Professional`
   - `Warm & Conversational`
   - `Concise & Direct`
4. Select `PDF` or `DOCX` output.
5. Generate cover letters.
6. Review the match analysis, reviewer scores, approval status, and cover-letter preview for each job.
7. Download individual files or all successful files as a ZIP archive.
8. Start another generation run with `Start Again`.

The local URL is normally `http://localhost:8501`.

## Local Folder Workflow

The non-web entry point reads files from the project folders and generates PDF files by default:

```powershell
python -m app.main
```

Use these folders for the local workflow:

```text
Resume/       One resume DOCX file
NewJobs/      One or more job-description DOCX files
CoverLetters/ Generated output files
```

The Streamlit workflow uses temporary files for uploaded documents and does not require these folders.

## Input Files

The web interface accepts Microsoft Word `.docx` files:

- One resume file.
- One or more job-description files.

The DOCX reader extracts non-empty paragraphs and text from tables. It does not explicitly extract images, headers, footers, text boxes, or other non-paragraph Word content.

## Generated Files

Supported output formats are PDF and DOCX. Each letter includes structured sections for:

- Candidate contact details.
- Date.
- Hiring manager and company information.
- Greeting and opening.
- Body paragraphs.
- Closing and sign-off.

Output names follow this pattern:

```text
<CandidateName>-CoverLetter-<CompanyName>.pdf
<CandidateName>-CoverLetter-<CompanyName>.docx
```

Characters other than letters and numbers are removed from candidate and company names when creating filenames. The Streamlit interface also creates a ZIP containing all successful files.

## AI Agents

All agents use the OpenAI Python client and the Responses API with structured Pydantic output parsing. The configured model is `gpt-5.6-luna`.

### Resume Agent

`app/agents/resume_agent.py` and `analyze_resume()` convert resume text into a `CandidateProfile`, including contact details, work experience, skills, qualifications, and achievements. The resume is treated as the source of truth and the agent is instructed not to invent or exaggerate information.

### Job Agent

`app/agents/job_agent.py` and `analyze_job()` convert job-description text into a `JobAnalysis`, including required and preferred skills, responsibilities, qualifications, company values, priorities, and customer expectations.

### Matching Agent

`app/agents/matching_agent.py` and `match_candidate_to_job()` produce:

- Direct matches.
- Transferable skills.
- Development areas.
- Recommended cover-letter focus.
- Unsupported requirements.

The matching instructions require conservative, evidence-based recommendations.

### Writer Agent

`app/agents/writer_agent.py` and `write_cover_letter()` create the structured cover letter. The writer validates the selected style, targets approximately 350 to 500 words and 3 to 5 body paragraphs, uses New Zealand English, and is instructed not to invent candidate facts, metrics, qualifications, or experience.

### Reviewer Agent

`app/agents/reviewer_agent.py` and `review_cover_letter()` review the generated letter against the resume, job analysis, match analysis, and selected style. It scores accuracy, relevance, naturalness, and professionalism from 1 to 10.

The reviewer also checks unsupported claims, generic AI language, repetition, style consistency, and New Zealand English. It returns a revised letter. The service exports the reviewed letter even when the reviewer does not approve it, so inspect the result before sending it.

## Project Structure

```text
app/
  agents/       Resume, job, matching, writer, and reviewer agents
  document/     DOCX reader plus PDF and DOCX writers
  models/       Pydantic data schemas
  services/     Cover-letter workflow orchestration
  web/          Streamlit interface
Resume/         Local resume files; ignored by Git
NewJobs/        Local job files; ignored by Git
CoverLetters/   Generated files; ignored by Git
```

Important modules:

- `app/web/app.py`: Streamlit interface and upload workflow.
- `app/services/cover_letter_service.py`: End-to-end generation pipeline.
- `app/document/reader.py`: DOCX paragraph and table extraction.
- `app/document/pdf_writer.py`: PDF export.
- `app/document/docx_writer.py`: DOCX export.
- `app/models/schemas.py`: Shared structured response models.
- `app/main.py`: Local-folder entry point.

## Setup

Requirements:

- Python 3.11 or newer.
- An OpenAI API key.

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a local environment file:

```powershell
Copy-Item .env.example .env
```

Set the key in `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

The application loads the key with `python-dotenv`. Never commit `.env`, paste the key into source code, or expose the key in screenshots or logs. The repository `.gitignore` excludes `.env`, virtual environments, Python cache files, local input documents, and generated cover letters.

## Tests and Diagnostics

The repository contains scripts named `test_*.py` for the agents, document writers, and OpenAI connectivity. They are primarily live integration and smoke scripts rather than a fully mocked unit-test suite. Many read files from `Resume/` and `NewJobs/`, call the live OpenAI API, and print results.

Run the test scripts through pytest when the required local files and API key are available:

```powershell
python -m pytest app
```

The OpenAI connectivity script is:

```powershell
python app/test_openai.py
```

These checks can consume API credits and depend on the configured model and available DOCX fixtures.

## Privacy and Limitations

- Resume and job-description content, including personal information, is sent to OpenAI for analysis and generation.
- The application has no authentication, authorization, rate limiting, or multi-user isolation.
- Files are accepted based on the `.docx` extension and may fail if malformed or unsupported.
- Only DOCX paragraphs and tables are extracted.
- AI output can contain inaccuracies even with source-of-truth prompts and reviewer checks. Review every letter before using it.
- Failed job exception details may be displayed in the Streamlit interface.
- The interface uses custom HTML styling. Treat model-generated or document-derived content as untrusted.
- Processing uses temporary uploaded files in the web workflow; it does not persist them into the repository input folders.
- Several model calls are made per job, so cost and latency increase with the number of job descriptions.
- Different candidate or company names can produce the same normalized output filename.