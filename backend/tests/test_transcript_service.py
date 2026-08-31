from app.services.transcript_service import _get_preferred_transcript_languages, detect_transcript_language


def test_detect_transcript_language_handles_hindi_text() -> None:
    transcript = "नमस्ते, आज हम Python के बारे में सीखेंगे। यह एक शक्तिशाली भाषा है।"
    assert detect_transcript_language(transcript) == "Hindi"


def test_preferred_transcript_languages_prioritize_hindi() -> None:
    languages = _get_preferred_transcript_languages()
    assert languages[0] == "hi"
    assert languages[1] == "hi-IN"
