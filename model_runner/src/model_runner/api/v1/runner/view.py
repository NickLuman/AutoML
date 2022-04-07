from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from .models import BestReports, Metadata
from .core import fit_best_models

runner_router = APIRouter(prefix="/runner", tags=["runner"])


@runner_router.post(
    "/fit_models",
    response_model=BestReports,
    status_code=201,
)
async def fit_best_models_view(
    data_file: UploadFile = File(...), metadata_raw: bytes = Form(...)
):
    try:
        metadata = Metadata.parse_raw(metadata_raw)
    except ValidationError as exc:
        raise HTTPException(
            detail=jsonable_encoder(exc.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        ) from exc
    best_reports = await fit_best_models(metadata, data_file)
    return best_reports
