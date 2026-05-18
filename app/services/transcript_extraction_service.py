import os
import json

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig, WebshareProxyConfig

from app.utils.paths import TRANSCRIPT_STORAGE_PATH


from app.models.schemas.transcript_schema import (
    TranscriptSegment,
    TranscriptResponse,
    ErrorResponse
)

TRANSCRIPT_STORAGE_PATH.mkdir(parents=True, exist_ok=True)


def _build_transcript_api() -> YouTubeTranscriptApi:
    webshare_username = os.getenv("WEBSHARE_PROXY_USERNAME")
    webshare_password = os.getenv("WEBSHARE_PROXY_PASSWORD")
    webshare_locations = os.getenv("WEBSHARE_PROXY_LOCATIONS")

    if webshare_username and webshare_password:
        locations = None
        if webshare_locations:
            locations = [
                location.strip().lower()
                for location in webshare_locations.split(",")
                if location.strip()
            ]

        return YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username=webshare_username,
                proxy_password=webshare_password,
                filter_ip_locations=locations,
            )
        )

    http_proxy = os.getenv("TRANSCRIPT_HTTP_PROXY")
    https_proxy = os.getenv("TRANSCRIPT_HTTPS_PROXY")

    if http_proxy or https_proxy:
        return YouTubeTranscriptApi(
            proxy_config=GenericProxyConfig(
                http_url=http_proxy,
                https_url=https_proxy or http_proxy,
            )
        )

    return YouTubeTranscriptApi()


def extract_transcript(video_id: str):

    try:

        api = _build_transcript_api()

        transcript_list = api.list(video_id)
        first_transcript = next(iter(transcript_list))
        transcript_data = first_transcript.fetch()

        segments = [
            TranscriptSegment(
                start=item.start,
                duration=item.duration,
                text=item.text
            )
            for item in transcript_data
        ]
        response = TranscriptResponse(
            video_id=video_id,
            transcript=segments
        )
        file_path = TRANSCRIPT_STORAGE_PATH / f"{video_id}.json"
        with open(file_path, "w") as f:
            json.dump(response.model_dump(), f, indent=4)

        return response
    
    
    except Exception as e:
        return ErrorResponse(
            error=str(e)
        )
