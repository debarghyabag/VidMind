from youtube_transcript_api import YouTubeTranscriptApi
import json
from pathlib import Path
from app.utils.paths import FILE_STORAGE_PATH


from app.models.schemas.transcript_schema import (
    TranscriptSegment,
    TranscriptResponse,
    ErrorResponse
)

FILE_STORAGE_PATH.mkdir(parents=True, exist_ok=True)


def extract_transcript(video_id: str):

    try:

        api = YouTubeTranscriptApi()

        transcript_list = api.list(video_id)
        first_transcript = next(iter(transcript_list))
        transcript_data = first_transcript.fetch()

        segments = [
            TranscriptSegment(
                start=item.start,
                duration=item.duration,
                text=item.text
            )
            for item in transcript_data
        ]
        response = TranscriptResponse(
            video_id=video_id,
            transcript=segments
        )
        file_path = FILE_STORAGE_PATH / f"{video_id}.json"
        with open(file_path, "w") as f:
            json.dump(response.model_dump(), f, indent=4)

        return response
    
    
    except Exception as e:
        return ErrorResponse(
            error=str(e)
        )