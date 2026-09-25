from pydantic import BaseModel, Field


class WorkExperience(BaseModel):
    job_title: str
    company: str
    dates: str
    responsibilities: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)


class CandidateProfile(BaseModel):
    name: str
    address: str = ""
    phone: str = ""
    email: str = ""
    professional_summary: str
    current_role: str
    current_company: str

    work_experience: list[WorkExperience] = Field(default_factory=list)

    skills: list[str] = Field(default_factory=list)
    qualifications: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)

class JobAnalysis(BaseModel):
    company: str
    role: str

    responsibilities: list[str] = Field(default_factory=list)
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)

    qualifications: list[str] = Field(default_factory=list)
    key_values: list[str] = Field(default_factory=list)
    customer_expectations: list[str] = Field(default_factory=list)

class CandidateJobMatch(BaseModel):
    strong_matches: list[str] = Field(default_factory=list)
    transferable_skills: list[str] = Field(default_factory=list)
    development_areas: list[str] = Field(default_factory=list)
    recommended_focus: list[str] = Field(default_factory=list)
    unsupported_requirements: list[str] = Field(default_factory=list)

class CoverLetter(BaseModel):
    greeting: str
    opening: str
    body: list[str] = Field(default_factory=list)
    closing: str
    sign_off: str

class ReviewResult(BaseModel):
    approved: bool

    accuracy_score: int
    relevance_score: int
    naturalness_score: int
    professionalism_score: int

    issues: list[str] = Field(default_factory=list)
    improvements: list[str] = Field(default_factory=list)

    revised_cover_letter: CoverLetter