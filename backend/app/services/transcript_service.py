"""Service for retrieving YouTube transcripts."""

import re

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (NoTranscriptFound, TranscriptsDisabled,
                                            VideoUnavailable)

from app.utils.youtube import extract_video_id


def detect_transcript_language(transcript: str) -> str:
    """Detect the transcript language from its script."""
    if re.search(r"[\u0900-\u097F]", transcript):
        return "Hindi"
    return "English"


def _get_preferred_transcript_languages() -> list[str]:
    """Return ordered language codes, preferring Hindi and English variants."""
    return ["hi", "en", "en-IN", "en-US", "hi-IN", "ta", "te", "mr", "bn", "gu"]


class TranscriptService:
    """Fetches and sanitizes YouTube transcripts."""

    def fetch_transcript(self, url: str) -> str:
        video_id = extract_video_id(url)
        if not video_id:
            raise ValueError("The provided YouTube URL is invalid.")

        api = YouTubeTranscriptApi()

        try:
            transcript_entries = api.fetch(video_id, languages=_get_preferred_transcript_languages())
        except NoTranscriptFound:
            try:
                transcript_list = api.list(video_id)
                available = [t.language_code for t in transcript_list]
                for lang in _get_preferred_transcript_languages():
                    if lang in available:
                        transcript_entries = transcript_list.find_transcript([lang]).fetch()
                        break
                else:
                    transcript_entries = transcript_list.find_generated_transcript(available).fetch()
            except (TranscriptsDisabled, VideoUnavailable, NoTranscriptFound) as exc:
                raise RuntimeError("No transcript was found for this video.") from exc
        except (TranscriptsDisabled, VideoUnavailable) as exc:
            raise RuntimeError("No transcript was found for this video.") from exc

        return "\n".join(
            entry.text for entry in transcript_entries if getattr(entry, "text", None)
        )

    def detect_transcript_language(self, transcript: str) -> str:
        """Public helper for the summary pipeline to detect transcript language."""
        return detect_transcript_language(transcript)
