"""Request models for the summary API."""

from pydantic import BaseModel, Field, HttpUrl


class SummaryRequest(BaseModel):
    """Request payload containing the YouTube URL."""

    url: HttpUrl = Field(..., description="The full YouTube video URL")
