from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from fastapi.encoders import jsonable_encoder
from loguru import logger
from pydantic import ValidationError

from .core import search_best_models
from .models import BestReports, Metadata

runner_router = APIRouter(prefix="/runner", tags=["runner"])


@runner_router.post(
    "/search_best_models",
    response_model=BestReports,
    status_code=status.HTTP_200_OK,
)
async def search_best_models_view(
    metadata_raw: str = Form(...), data_file: UploadFile = File(...)
):
    try:
        metadata = Metadata.parse_raw(metadata_raw)
    except ValidationError as exc:
        raise HTTPException(
            detail=jsonable_encoder(exc.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        ) from exc
    best_reports = await search_best_models(metadata, data_file)
    return best_reports
