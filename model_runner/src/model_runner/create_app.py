import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .api.app_status import status_router
from .api.v1.runner.view import runner_router
from .external.minio.minio_utils import connect_to_minio

app = FastAPI(
    title="AutoML Model Runner V1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    version=os.getenv("APP_VERSION", default="DEV"),
)

logger_config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<level>{level}: {message}</level>",
        }
    ]
}


def create_app():
    logger.configure(**logger_config)
    app.include_router(status_router)
    app.include_router(runner_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", connect_to_minio)

    return app
