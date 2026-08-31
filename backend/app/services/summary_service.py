"""Application service orchestrating transcript retrieval and summarization."""

from app.chains.summary_chain import build_summary_chain
from app.models.response import SummaryResponse
from app.services.transcript_service import TranscriptService


MAX_TRANSCRIPT_CHARS = 12000


class SummaryService:
    """Coordinates the summary workflow."""

    def __init__(self, transcript_service: TranscriptService | None = None) -> None:
        self.transcript_service = transcript_service or TranscriptService()
        self.summary_chain = None

    def _get_summary_chain(self):
        if self.summary_chain is None:
            self.summary_chain = build_summary_chain()
        return self.summary_chain

    def _prepare_transcript_for_model(self, transcript: str) -> str:
        """Trim transcript content to fit within the Groq context budget."""
        if len(transcript) <= MAX_TRANSCRIPT_CHARS:
            return transcript

        truncated = transcript[:MAX_TRANSCRIPT_CHARS].rsplit(" ", 1)[0]
        return (
            "Transcript truncated to fit the model context window. "
            "Key details beyond this point were omitted to avoid token-limit errors.\n\n"
            f"{truncated}"
        )

    def summarize(self, url: str) -> SummaryResponse:
        transcript = self.transcript_service.fetch_transcript(url)
        transcript = self._prepare_transcript_for_model(transcript)
        language = self.transcript_service.detect_transcript_language(transcript)
        result = self._get_summary_chain().invoke({"transcript": transcript, "language": language})
        if isinstance(result, SummaryResponse):
            return result

        payload = dict(result)
        payload.setdefault("title", "YouTube Video Summary")
        return SummaryResponse(**payload)
