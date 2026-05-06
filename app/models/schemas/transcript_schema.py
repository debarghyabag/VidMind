from pydantic import BaseModel
from typing import List


class TranscriptSegment(BaseModel):
    start: float
    duration: float
    text: str


class TranscriptResponse(BaseModel):
    video_id: str
    transcript: List[TranscriptSegment]


class ErrorResponse(BaseModel):
    error: str