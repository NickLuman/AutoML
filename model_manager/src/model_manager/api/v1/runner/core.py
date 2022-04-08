from io import StringIO

from fastapi import File
from loguru import logger

from .models import Metadata, BestReports
from ....external.model_runner.requests import send_fit_models


async def search_best_models(metadata: Metadata, data_file: File) -> BestReports:
    files = {"data_file": data_file.file.read()}
    reports = await send_fit_models(metadata.dict(), files)

    return reports
