from fastapi import FastAPI
from app.api.router.video_id import router as video_id_router

app = FastAPI(
    title="VidMind API",
    description="AI-powered YouTube summarization backend",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "status": "running",
        "message": "VidMind backend is live"
    }

app.include_router(video_id_router)