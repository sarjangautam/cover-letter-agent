import os

from dotenv import load_dotenv
from openai import OpenAI

from app.models.schemas import CandidateProfile


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY was not found. "
        "Check your .env file."
    )

client = OpenAI(api_key=api_key)


def analyze_resume(resume_text: str) -> CandidateProfile:

    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=[
            {
                "role": "system",
                "content": """
You are a professional resume analysis agent.

Analyze the candidate's resume and extract accurate,
structured information.

IMPORTANT RULES:

1. The resume is the only source of truth.
2. Never invent information.
3. Extract the candidate's name, address, phone number,
    and email address when they are present.
4. Never add qualifications, skills, achievements,
   responsibilities, companies, job titles, or dates
   that are not supported by the resume.
5. Preserve the meaning of the resume.
6. If information is not available, use an empty value
   or an empty list.
7. Do not exaggerate the candidate's experience.
8. Extract information accurately so another AI agent
   can later use it to write job-specific cover letters.
""",
            },
            {
                "role": "user",
                "content": f"""
Please analyze the following resume and return
the candidate profile.

RESUME:

{resume_text}
""",
            },
        ],
        text_format=CandidateProfile,
    )

    return response.output_parsed