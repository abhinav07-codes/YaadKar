"""Response models for the summary API."""

from pydantic import BaseModel, Field


class SummaryResponse(BaseModel):
    """Structured summary returned to the client."""

    title: str = Field(..., description="Video title or fallback label")
    summary: str = Field(..., description="Short summary of the video")
    key_points: list[str] = Field(default_factory=list, description="Core concepts")
    detailed_explanation: list[str] = Field(
        default_factory=list,
        description="Very detailed explanatory notes that expand on the material deeply",
    )
    interview_questions: list[str] = Field(default_factory=list, description="Interview-style questions")
