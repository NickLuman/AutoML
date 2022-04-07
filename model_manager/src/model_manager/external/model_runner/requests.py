import httpx
import json
from loguru import logger

from ...settings import settings

model_runner_url = f"http://{settings.model_runner_host}:{settings.model_runner_port}"


async def send_fit_models(metadata: dict, files: dict) -> dict:
    timeout = httpx.Timeout(None, connect=600.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            files["metadata_raw"] = json.dumps(metadata).encode("utf-8")
            resp = await client.post(
                f"{model_runner_url}/runner/fit_models",
                files=files,
            )
        except Exception as exc:
            logger.warning("here")
            logger.error(exc)

        if not resp:
            logger.warning("got empty response")

        return resp.json()
