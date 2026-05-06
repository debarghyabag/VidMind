from youtube_transcript_api import YouTubeTranscriptApi

from app.models.schemas.transcript_schema import (
    TranscriptSegment,
    TranscriptResponse,
    ErrorResponse
)


def extract_transcript(video_id: str):

    try:

        api = YouTubeTranscriptApi()

        transcript_data = api.fetch(video_id)

        segments = [
            TranscriptSegment(
                start=item.start,
                duration=item.duration,
                text=item.text
            )
            for item in transcript_data
        ]

        return TranscriptResponse(
            video_id=video_id,
            transcript=segments
        )

    except Exception as e:
        return ErrorResponse(
            error=str(e)
        )