import os
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv(".env")

ASSET_ID = 537826862
INDEX_PATH = Path("data/processed/semantic_index.json")

API_URL = (
    f"https://api.github.com/repos/inetke/"
    f"revenue-ai-copilot-assets/releases/assets/{ASSET_ID}"
)


def download_semantic_index():
    token = os.getenv("GITHUB_ASSETS_TOKEN")

    if not token:
        raise RuntimeError(
            "GITHUB_ASSETS_TOKEN is not configured."
        )

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(
        API_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/octet-stream",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        stream=True,
        timeout=60,
    )

    response.raise_for_status()

    with open(INDEX_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    return INDEX_PATH