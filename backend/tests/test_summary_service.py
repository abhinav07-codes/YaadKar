from app.services.summary_service import SummaryService


def test_prepare_transcript_for_model_truncates_long_input() -> None:
    service = SummaryService()
    transcript = "word " * 30000

    prepared = service._prepare_transcript_for_model(transcript)

    assert len(prepared) < 15000
    assert "Transcript truncated" in prepared
