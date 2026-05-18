from app.utils.paths import CHUNKS_STORAGE_PATH
import json
import os
from app.utils.youtube import extract_video_id
from app.services.transcript_extraction_service import extract_transcript
from app.services.chunking_service import chunking_function
from app.models.schemas.transcript_schema import ErrorResponse
from app.utils.paths import *
from app.services.summarization_service import summarize_video
from app.services.product_specs_service import extract_product_specs




def get_video_transcript(video_id: str):


    if not video_id:
        return ErrorResponse(
            error="Invalid YouTube URL"
        )

    return extract_transcript(video_id)


def get_video_chunks(video_id : str):

    transcript_file_path = TRANSCRIPT_STORAGE_PATH / f"{video_id}.json"

    if not transcript_file_path.exists():
        transcript_response = extract_transcript(video_id)
        if isinstance(transcript_response, ErrorResponse):
            return transcript_response
        transcript = transcript_response.model_dump()["transcript"]
    else:
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

def get_video_summary(video_id : str):
    chunk_file_path = CHUNKS_STORAGE_PATH / f"{video_id}.json"
    if not chunk_file_path.exists():
        return ErrorResponse(
            error="Chunks not found for the given video ID"
        )
    
    with open(chunk_file_path, "r", encoding="utf-8") as f:
        chunk_data = json.load(f)
        chunks = chunk_data["chunks"]
    
    if not chunks:
        return ErrorResponse(
            error="No chunks found for the given video ID"
        )
    
    # Call the summarization service with the chunks
    summary = summarize_video(video_id, chunks)
    summary_file_path = SUMMARY_STORAGE_PATH / f"{video_id}.json"
    summary_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_file_path, "w", encoding="utf-8") as f:
        json.dump(summary.model_dump(), f, indent=4)

    return summary


def get_video_product_specs(video_id: str):
    chunk_file_path = CHUNKS_STORAGE_PATH / f"{video_id}.json"

    if not chunk_file_path.exists():
        chunk_response = get_video_chunks(video_id)
        if isinstance(chunk_response, ErrorResponse):
            return chunk_response
        chunks = chunk_response.model_dump()["chunks"]
    else:
        with open(chunk_file_path, "r", encoding="utf-8") as f:
            chunk_data = json.load(f)
            chunks = chunk_data["chunks"]

    if not chunks:
        return ErrorResponse(
            error="No chunks found for the given video ID"
        )

    product_specs = extract_product_specs(video_id, chunks)
    output_file_path = OUTPUT_STORAGE_PATH / f"{video_id}.json"
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(product_specs.model_dump(), f, indent=4)

    return product_specs
