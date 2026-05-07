from fastapi import APIRouter

from app.core.controller import *
from app.utils.youtube import extract_video_id as _extract_video_id

from app.models.schemas.transcript_schema import ErrorResponse
from app.models.schemas.video_details_schema import AnalyzeVideoRequest

router = APIRouter()


@router.post("/video/analyze")
async def analyze_video(request: AnalyzeVideoRequest):

    video_id = _extract_video_id(request.url)

    if not video_id:
        return ErrorResponse(
            error="Invalid YouTube URL"
        )

    return {
        "video_id": video_id
    }


@router.get("/video/{video_id}/transcript")
async def extract_transcript(video_id: str):

    if not video_id:
        return ErrorResponse(
            error="Invalid video ID"
        )

    return get_video_transcript(video_id)


@router.get("/video/{video_id}/chunks")
async def extract_chunks(video_id: str):

    if not video_id:
        return ErrorResponse(
            error="Invalid video ID"
        )

    return get_video_chunks(video_id)