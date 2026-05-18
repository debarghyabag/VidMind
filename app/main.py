import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router.video_api import router as video_id_router


app = FastAPI(
    title="VidMind API",
    description="AI-powered YouTube summarization backend",
    version="1.0.0"
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]
allow_credentials = "*" not in allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "status": "running",
        "message": "VidMind backend is live"
    }

app.include_router(video_id_router)
