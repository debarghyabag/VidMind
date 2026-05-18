from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
YOUTUBE_ID_PATH = BASE_DIR / "app/utils/youtube.py"
FILE_STORAGE_PATH = BASE_DIR / "app/data_storage"
TRANSCRIPT_STORAGE_PATH = FILE_STORAGE_PATH / "transcript_json"
CHUNKS_STORAGE_PATH = FILE_STORAGE_PATH / "chunking_json"
SUMMARY_STORAGE_PATH = FILE_STORAGE_PATH / "summary_json"
OUTPUT_STORAGE_PATH = FILE_STORAGE_PATH / "output"
