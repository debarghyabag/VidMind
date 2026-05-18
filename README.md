# VidMind

VidMind is a FastAPI-based backend service that transforms YouTube videos into structured, AI-ready data. It extracts video IDs from YouTube URLs, retrieves available transcripts, organizes transcript segments into timestamped chunks, generates concise summaries, and extracts structured product specifications from tech review videos for downstream analysis and storage.

The system is especially useful for converting long-form product reviews, comparisons, and technical discussions into clean JSON outputs that can power search, product comparison tools, recommendation systems, dashboards, or analytics workflows.

## Features

- Parse video IDs from common YouTube URL formats
- Fetch YouTube transcripts using `youtube-transcript-api`
- Store transcript data as JSON
- Group transcript segments into timestamped chunks
- Generate AI-powered video summaries
- Extract structured product specifications from tech review videos
- Support multiple products in a single video
- Save generated outputs under `app/data_storage`
- Expose a clean FastAPI API with interactive Swagger documentation

## Tech Stack

- Python
- FastAPI
- Pydantic
- LangChain
- Azure OpenAI
- YouTube Transcript API

## Project Structure

```text
app/
  api/router/          API routes
  core/                Request controllers
  models/schemas/      Pydantic response and request models
  services/            Transcript, chunking, summary, and extraction services
  utils/               Path and YouTube URL helpers
  data_storage/        Generated transcript, chunk, summary, and product JSON files
```

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv deb
deb\Scripts\activate
pip install -r requirements.txt
```

## Run the API

On Windows, you can start the backend with:

```bash
run_batch_file.bat
```

Or run FastAPI directly:

```bash
fastapi dev .\app\main.py
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Health Check

```http
GET /
```

Returns the backend status.

### Analyze a YouTube URL

```http
POST /video/analyze
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

Returns the extracted YouTube video ID.

### Extract Transcript

```http
GET /video/{video_id}/transcript
```

Fetches transcript segments for a video and stores the result as JSON.

### Generate Chunks

```http
GET /video/{video_id}/chunks
```

Groups transcript segments into timestamped chunks.

### Generate Summary

```http
GET /video/{video_id}/summary
```

Generates an AI-powered summary from the video's transcript chunks and saves it
to `app/data_storage/summary_json/{video_id}.json`.

### Extract Product Specifications

```http
GET /video/{video_id}/product-specs
```

Extracts one or more reviewed tech products from the video transcript and saves
the structured output to `app/data_storage/output/{video_id}.json`.

You can also extract directly from a YouTube URL:

```http
POST /video/product-specs
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

Example output:

```json
{
  "video_id": "VIDEO_ID",
  "products": [
    {
      "product_name": "Example Phone Pro",
      "brand": "Example",
      "category": "smartphone",
      "specifications": [
        {
          "name": "display",
          "value": "6.7 inch OLED"
        },
        {
          "name": "storage",
          "value": "256 GB"
        }
      ],
      "notable_features": [
        "Bright display",
        "Improved battery life"
      ],
      "price": "$999",
      "availability": null,
      "evidence": [
        "Transcript snippet used by the extractor"
      ]
    }
  ]
}
```

## Notes

- Transcript extraction depends on transcript availability for the target
  YouTube video.
- Generated data is stored under `app/data_storage`.
- Product specification output is stored under `app/data_storage/output`.
- Chunk generation expects transcript data to exist before chunks are created.
