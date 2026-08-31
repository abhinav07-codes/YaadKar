"""Application service orchestrating transcript retrieval and summarization."""

from app.chains.summary_chain import build_summary_chain
from app.models.response import SummaryResponse
from app.services.transcript_service import TranscriptService


class SummaryService:
    """Coordinates the summary workflow."""

    def __init__(self, transcript_service: TranscriptService | None = None) -> None:
        self.transcript_service = transcript_service or TranscriptService()
        self.summary_chain = None

    def _get_summary_chain(self):
        if self.summary_chain is None:
            self.summary_chain = build_summary_chain()
        return self.summary_chain

    def summarize(self, url: str) -> SummaryResponse:
        transcript = self.transcript_service.fetch_transcript(url)
        language = self.transcript_service.detect_transcript_language(transcript)
        result = self._get_summary_chain().invoke({"transcript": transcript, "language": language})
        if isinstance(result, SummaryResponse):
            return result

        payload = dict(result)
        payload.setdefault("title", "YouTube Video Summary")
        return SummaryResponse(**payload)
