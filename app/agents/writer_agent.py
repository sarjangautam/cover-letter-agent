import os

from dotenv import load_dotenv
from openai import OpenAI

from app.models.schemas import (
    CandidateJobMatch,
    CandidateProfile,
    CoverLetter,
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


def write_cover_letter(
    candidate: CandidateProfile,
    job: JobAnalysis,
    match: CandidateJobMatch,
    writing_style: str = "Professional",
) -> CoverLetter:

    # ---------------------------------------------------------
    # Validate writing style
    # ---------------------------------------------------------

    allowed_styles = {
        "Professional",
        "Warm & Conversational",
        "Concise & Direct",
    }

    if writing_style not in allowed_styles:
        raise ValueError(
            f"Unsupported writing style: {writing_style}. "
            f"Choose one of: {', '.join(sorted(allowed_styles))}"
        )

    # ---------------------------------------------------------
    # Generate cover letter
    # ---------------------------------------------------------

    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=[
            {
                "role": "system",
                "content": """
You are an expert professional cover-letter writer.

Your job is to write a tailored cover letter using:

1. The candidate profile.
2. The job analysis.
3. The candidate-to-job matching analysis.

The cover letter must be natural, professional,
specific to the role, and believable.

IMPORTANT RULES:

ACCURACY
- The candidate profile is the source of truth.
- Never invent employment history.
- Never invent qualifications.
- Never invent achievements.
- Never invent responsibilities.
- Never invent metrics or results.
- Never claim the candidate has experience that is
  not supported by the candidate profile.
- Do not turn a transferable skill into a claim of
  direct experience.
- Do not assume experience simply because the job
  description requests it.
- Do not add certifications, licences, education,
  technical skills, management experience, or
  industry experience unless supported by the
  candidate profile.

RELEVANCE
- Focus on the strongest matches identified by the
  Matching Agent.
- Explain why the candidate's experience is relevant
  to this particular role.
- Use the company's values or priorities when relevant.
- Do not simply repeat the job description.
- Do not simply list the candidate's previous duties.
- Prioritise information that helps demonstrate
  suitability for this specific role.

STYLE

The selected writing style is provided separately in
the user request.

Adapt the tone and wording to the selected style while
keeping the letter professional, natural, accurate,
and appropriate for a job application in New Zealand.

Available writing styles:

Professional:
- Polished, clear and business-focused.
- Confident and professional without sounding overly formal.
- Suitable as the default style for most applications.

Warm & Conversational:
- Professional but more personable and approachable.
- Use natural, friendly language.
- Allow the candidate's personality to come through
  without becoming casual or informal.
- Avoid sounding overly scripted or corporate.

Concise & Direct:
- Focused, straightforward and efficient.
- Remove unnecessary wording and repetition.
- Make the candidate's relevant experience and value
  clear quickly.
- Avoid long introductions or unnecessary background.

For every style:
- Use natural New Zealand English.
- Sound like a real professional person.
- Be confident but not arrogant.
- Be warm and respectful.
- Avoid excessive corporate language.
- Avoid clichés and generic AI wording.
- Avoid repetitive sentence structures.
- Avoid unnecessarily complicated vocabulary.
- Do not make the letter sound robotic.
- Do not use exaggerated claims.
- Do not make claims that cannot be supported by
  the candidate profile.

Avoid generic phrases such as:
- "I am thrilled to apply"
- "I am uniquely positioned"
- "I am excited to leverage"
- "I am confident that I would be an excellent fit"
- "I believe I am the perfect candidate"
- "I am passionate about delivering exceptional results"

Only use similar wording if it genuinely fits the
candidate and sounds natural in context.

STRUCTURE
- Start with a strong, natural opening.
- Clearly identify the role being applied for.
- Mention the company naturally.
- Explain relevant experience and skills.
- Connect the candidate's background to the role.
- Use specific evidence from the candidate profile.
- Explain genuine motivation for the opportunity.
- Finish with a professional closing.
- Avoid simply repeating the resume.
- Avoid simply copying language from the job description.

LENGTH
- Aim for approximately 350-500 words.
- Use 3-5 body paragraphs.
- Keep paragraphs reasonably short.
- Avoid unnecessary repetition.

PERSONALISATION
- Mention the company and role naturally.
- Make the letter clearly specific to this job.
- Use the strongest relevant candidate experience.
- Connect the candidate's background to the employer's
  needs where the evidence supports that connection.
- Avoid generic statements that could apply to any company.

TRANSFERABLE SKILLS
- Transferable skills may be discussed when appropriate.
- Clearly distinguish transferable skills from direct
  experience.
- Never present a transferable skill as direct experience
  in an industry, system, role, or responsibility that
  is not supported by the candidate profile.

MISSING REQUIREMENTS
- If the candidate does not meet a requirement,
  do not hide that by inventing experience.
- Do not explicitly draw unnecessary attention to every
  missing requirement.
- Instead, focus on relevant experience and transferable
  skills where appropriate.

SIGN-OFF
- The sign_off field must contain only the closing phrase.
- Examples:
  "Yours sincerely,"
  "Kind regards,"
- Do NOT include the candidate's name in sign_off.
- The candidate's name will be added separately by the
  PDF generation process.
""",
            },
            {
                "role": "user",
                "content": f"""
Write a tailored cover letter for this candidate.

SELECTED WRITING STYLE:

{writing_style}

Use this style to influence the tone, wording,
sentence structure, and level of conciseness.

The selected style must NOT change, exaggerate,
or invent any candidate facts.


CANDIDATE PROFILE:

{candidate.model_dump_json(indent=2)}


JOB ANALYSIS:

{job.model_dump_json(indent=2)}


CANDIDATE → JOB MATCH:

{match.model_dump_json(indent=2)}


Create the final cover letter using only supported
candidate information.

The cover letter should:

- Be specific to the company and role.
- Focus on the strongest relevant matches.
- Use natural New Zealand English.
- Sound like a real person wrote it.
- Reflect the selected writing style.
- Avoid generic AI language.
- Avoid simply copying the job description.
- Avoid simply repeating the resume.
- Never invent information.

Remember:
The candidate profile is the source of truth.
""",
            },
        ],
        text_format=CoverLetter,
    )

    return response.output_parsed