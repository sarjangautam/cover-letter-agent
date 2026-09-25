import os

from dotenv import load_dotenv
from openai import OpenAI

from app.models.schemas import JobAnalysis


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY was not found. "
        "Check your .env file."
    )

client = OpenAI(api_key=api_key)


def analyze_job(job_text: str) -> JobAnalysis:

    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=[
            {
                "role": "system",
                "content": """
You are a professional job description analysis agent.

Analyze the job description and extract accurate,
structured information.

IMPORTANT RULES:

1. Use only information contained in the job description.
2. Never invent requirements.
3. Separate required skills from preferred skills.
4. Identify the main responsibilities of the role.
5. Identify qualifications or certifications mentioned.
6. Identify the company's values or priorities when they
   are explicitly stated or clearly described.
7. Identify important customer expectations.
8. Do not assume that a requirement is mandatory unless
   the job description indicates that it is.
9. Keep the extracted information concise and useful for
   another AI agent that will later match a candidate
   against this job.
""",
            },
            {
                "role": "user",
                "content": f"""
Please analyze the following job description.

JOB DESCRIPTION:

{job_text}
""",
            },
        ],
        text_format=JobAnalysis,
    )

    return response.output_parsed