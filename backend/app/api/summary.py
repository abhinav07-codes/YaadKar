"""API routes for summarization."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.request import SummaryRequest
from app.models.response import SummaryResponse
from app.services.summary_service import SummaryService

router = APIRouter(prefix="/summarize", tags=["summary"])


def get_summary_service() -> SummaryService:
    """Create a summary service instance for each request."""
    return SummaryService()


@router.post("", response_model=SummaryResponse, status_code=status.HTTP_200_OK)
def summarize_video(
    payload: SummaryRequest,
    service: SummaryService = Depends(get_summary_service),
) -> SummaryResponse:
    try:
        return service.summarize(str(payload.url))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
