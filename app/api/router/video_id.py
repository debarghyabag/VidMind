from fastapi import APIRouter
from app.utils.youtube import extract_video_id as _extract_video_id

router = APIRouter()


@router.get("/extract_video_id")
async def extract_video_id(url: str):
    return {"video_id": _extract_video_id(url)}