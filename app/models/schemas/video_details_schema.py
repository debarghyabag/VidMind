from pydantic import BaseModel


class AnalyzeVideoRequest(BaseModel):
    url: str