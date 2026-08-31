from app.services.transcript_service import detect_transcript_language
from app.utils.youtube import extract_video_id


def test_extract_video_id_from_watch_url() -> None:
    assert extract_video_id("https://www.youtube.com/watch?v=abc123xyz") == "abc123xyz"


def test_extract_video_id_from_short_url() -> None:
    assert extract_video_id("https://youtu.be/xyz789") == "xyz789"


def test_detect_transcript_language_handles_hindi_text() -> None:
    transcript = "नमस्ते, आज हम Python के बारे में सीखेंगे। यह एक शक्तिशाली भाषा है।"
    assert detect_transcript_language(transcript) == "Hindi"
