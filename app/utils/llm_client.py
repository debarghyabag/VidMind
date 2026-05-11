import os
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from app.utils.paths import BASE_DIR

load_dotenv(BASE_DIR / "app" / ".env")

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("llm_endpoint_deb_gpt5"),
    api_key=os.getenv("api_key_deb_gpt5"),
    api_version=os.getenv("api_version_deb_gpt5"),
    )
