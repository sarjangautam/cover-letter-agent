import os

from dotenv import load_dotenv
from openai import OpenAI

from app.models.schemas import (
    CandidateJobMatch,
    CandidateProfile,
    JobAnalysis,
)


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY was not found. "
        "Check your .env file."
    )

client = OpenAI(api_key=api_key)


def match_candidate_to_job(
    candidate: CandidateProfile,
    job: JobAnalysis,
) -> CandidateJobMatch:

    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=[
            {
                "role": "system",
                "content": """
You are a professional recruitment matching agent.

Your job is to compare a candidate's resume profile
against a job analysis and identify the strongest,
most relevant connections.

IMPORTANT RULES:

1. The candidate profile is the source of truth for
   the candidate's experience.

2. The job analysis is the source of truth for the
   job requirements.

3. Never invent candidate experience.

4. Never assume the candidate has a skill simply
   because the job requires it.

5. Identify direct matches where the candidate's
   actual experience clearly relates to the job.

6. Identify transferable skills when the candidate
   does not have direct experience but has relevant
   experience that can reasonably transfer.

7. Identify development areas where the job asks for
   something that is not clearly supported by the
   candidate profile.

8. Identify unsupported requirements explicitly.

9. Recommend the strongest topics that the cover
   letter should focus on.

10. Do not recommend claiming unsupported experience.

11. Be conservative and evidence-based.

The purpose of this analysis is to provide reliable
evidence to a later cover-letter-writing agent.
""",
            },
            {
                "role": "user",
                "content": f"""
Compare the candidate with the job.

CANDIDATE PROFILE:

{candidate.model_dump_json(indent=2)}


JOB ANALYSIS:

{job.model_dump_json(indent=2)}


Return the strongest matches, transferable skills,
development areas, recommended cover-letter focus,
and unsupported requirements.
""",
            },
        ],
        text_format=CandidateJobMatch,
    )

    return response.output_parsed