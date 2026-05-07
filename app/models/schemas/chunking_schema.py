from pydantic import BaseModel

class Chunk(BaseModel):
    start_time : float
    end_time : float
    text : str

class ChunkResponse(BaseModel):
    video_id : str
    chunks : list[Chunk]