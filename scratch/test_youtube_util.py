from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """extract video ID from YouTube URL and return it"""
    parsed_url = urlparse(url)
    print(f"URL: {url}")
    print(f"Hostname: {parsed_url.hostname}")
    print(f"Path: {parsed_url.path}")
    if parsed_url.hostname in ["www.youtube.com", "youtube.com", "m.youtube.com"]:
        if parsed_url.path == "/watch":
            query_params = parse_qs(parsed_url.query)
            return query_params.get("v", [None])[0]
        elif parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/")[2]
        elif parsed_url.path.startswith("/v/"):
            return parsed_url.path.split("/")[2]
    elif parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    return None

print(f"Result: {extract_video_id('2HIJlD46Kig')}")
