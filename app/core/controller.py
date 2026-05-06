from app.utils.youtube import extract_video_id
from app.services.transcript_extraction_service import extract_transcript
from app.models.schemas.transcript_schema import ErrorResponse


def get_video_transcript(video_id: str):


    if not video_id:
        return ErrorResponse(
            error="Invalid YouTube URL"
        )

    return extract_transcript(video_id)