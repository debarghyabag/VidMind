from app.utils.paths import CHUNKS_STORAGE_PATH
import json
import os
from app.utils.youtube import extract_video_id
from app.services.transcript_extraction_service import extract_transcript
from app.services.chunking_service import chunking_function
from app.models.schemas.transcript_schema import ErrorResponse
from app.utils.paths import *




def get_video_transcript(video_id: str):


    if not video_id:
        return ErrorResponse(
            error="Invalid YouTube URL"
        )

    return extract_transcript(video_id)


def get_video_chunks(video_id : str):

    transcript_file_path = TRANSCRIPT_STORAGE_PATH / f"{video_id}.json"
    with open(transcript_file_path, "r", encoding="utf-8") as f:
        transcript_data = json.load(f)
        transcript = transcript_data["transcript"]
    if not transcript:
        return ErrorResponse(
            error="Invalid transcript"
        )
    
    chunk_file_path = CHUNKS_STORAGE_PATH / f"{video_id}.json"
    chunking_service_output = chunking_function(video_id, transcript)
    chunk_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(chunk_file_path, "w", encoding = "utf-8") as f:
        json.dump(chunking_service_output.model_dump(), f, indent=4)
    return chunking_service_output