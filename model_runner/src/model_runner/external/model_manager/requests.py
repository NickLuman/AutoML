import httpx
from loguru import logger

from ...settings import settings

model_manager_url = (
    f"http://{settings.model_manager_host}:{settings.model_manager_port}"
)


async def get_model_by_name(name: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{model_manager_url}/model/{name}")
        if not resp:
            logger.warning("got empty response")

        return resp.json()
