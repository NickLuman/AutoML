import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from loguru import logger

from .api.app_status import status_router
from .api.v1.model_versions.views import model_versions_router
from .api.v1.models.views import models_router
from .api.v1.projects.views import projects_router
from .api.v1.runner.view import runner_router
from .api.v1.users.views import users_router
from .external.minio.minio_utils import connect_to_minio
from .external.postgres.db import SQLALCHEMY_DATABASE_URL

app = FastAPI(
    title="AutoML Model Manager V1",
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
    app.include_router(users_router)
    app.include_router(projects_router)
    app.include_router(models_router)
    app.include_router(model_versions_router)
    app.include_router(runner_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        DBSessionMiddleware,
        db_url=SQLALCHEMY_DATABASE_URL,
    )

    app.add_event_handler("startup", connect_to_minio)

    return app
