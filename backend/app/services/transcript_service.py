"""Service for retrieving YouTube transcripts."""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable, NoTranscriptFound

from app.utils.youtube import extract_video_id


class TranscriptService:
    """Fetches and sanitizes YouTube transcripts."""

    def fetch_transcript(self, url: str) -> str:
        video_id = extract_video_id(url)
        if not video_id:
            raise ValueError("The provided YouTube URL is invalid.")

        try:
            transcript_entries = YouTubeTranscriptApi().fetch(video_id)
        except (TranscriptsDisabled, VideoUnavailable, NoTranscriptFound) as exc:
            raise RuntimeError("No transcript was found for this video.") from exc

        return "\n".join(
            entry.text for entry in transcript_entries if getattr(entry, "text", None)
        )
