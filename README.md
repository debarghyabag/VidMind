# VidMind

VidMind is a FastAPI backend for working with YouTube videos. It can extract a
video ID from a YouTube URL, fetch the video's transcript, and group transcript
segments into timestamped chunks.

## Features

- Parse video IDs from common YouTube URL formats.
- Fetch transcripts with `youtube-transcript-api`.
- Return timestamped transcript segments.
- Generate transcript chunks for downstream summarization or analysis.
- Extract tech product specifications from review videos into structured JSON.
- Expose a simple FastAPI API with interactive docs.

## Project Structure

```text
app/
  api/router/          API routes
  core/                Request controllers
  models/schemas/      Pydantic response and request models
  services/            Transcript extraction and chunking logic
  utils/               Path and YouTube URL helpers
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
