import os
from urllib.parse import urlparse

from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from app.utils.paths import BASE_DIR

load_dotenv(BASE_DIR / "app" / ".env")


def _azure_config_from_env() -> tuple[str | None, str | None]:
    endpoint = os.getenv("llm_endpoint_deb_gpt5")
    deployment = os.getenv("llm_deployment_deb_gpt5")

    if not endpoint:
        return None, deployment

    parsed = urlparse(endpoint)
    path_parts = [part for part in parsed.path.split("/") if part]

    if "deployments" in path_parts:
        deployment_index = path_parts.index("deployments") + 1
        if deployment_index < len(path_parts):
            deployment = deployment or path_parts[deployment_index]
        endpoint = f"{parsed.scheme}://{parsed.netloc}"

    return endpoint, deployment


azure_endpoint, azure_deployment = _azure_config_from_env()

llm = AzureChatOpenAI(
    azure_endpoint=azure_endpoint,
    azure_deployment=azure_deployment,
    api_key=os.getenv("api_key_deb_gpt5"),
    api_version=os.getenv("api_version_deb_gpt5"),
)
