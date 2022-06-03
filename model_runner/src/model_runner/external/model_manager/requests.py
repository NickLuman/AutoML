import json

import httpx
from loguru import logger

from ...settings import settings

model_manager_url = (
    f"http://{settings.model_manager_host}:{settings.model_manager_port}"
)


async def get_model_by_name(name: str) -> dict:
    async with httpx.AsyncClient() as client:
        auth = await client.post(
            f"{model_manager_url}/api/v1/users/login/token",
            data=json.dumps(
                {
                    "username": settings.model_manager_username,
                    "password": settings.model_manager_password,
                }
            ),
        )
        resp = await client.get(f"{model_manager_url}/api/v1/model-versions/{name}")
        if not resp:
            logger.warning("got empty response")

        return resp.json()
