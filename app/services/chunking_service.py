from app.models.schemas.chunking_schema import Chunk, ChunkResponse



def chunking_function(video_id : str, transcript : list):
    chunks = []
    for i in range (0, len(transcript), 3):
        current_chunk = transcript[i:i+3]
        start_time = current_chunk[0]["start"]
        end_time = current_chunk[-1]["start"] + current_chunk[-1]["duration"]
        combined_text = " ". join(segment["text"] for segment in current_chunk)
        chunk_object = Chunk(start_time = start_time, end_time = end_time, text = combined_text)
        chunks.append(chunk_object)

    return ChunkResponse(video_id=video_id, chunks=chunks)

 
    