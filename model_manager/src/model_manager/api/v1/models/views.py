from fastapi import APIRouter, UploadFile, File, Form

from .core import create_model
from .models import CreateModel, Model

model_router = APIRouter(prefix="/model", tags=["model"])


@model_router.post(
    "/",
    response_model=int,
    status_code=201,
)
async def add_model(model_raw: str = Form(...), model_zip: UploadFile = File(...)):
    id = create_model(model_raw, model_zip)
    return id
