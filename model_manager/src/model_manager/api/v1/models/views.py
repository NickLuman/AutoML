from os import stat

from fastapi import APIRouter, File, Form, UploadFile, status

from .core import create_model, get_model_by_name
from .models import GetModel

model_router = APIRouter(prefix="/api/v1/model", tags=["model"])


@model_router.post(
    "/",
    response_model=int,
    status_code=status.HTTP_201_CREATED,
)
async def add_model(model_raw: str = Form(...), model_zip: UploadFile = File(...)):
    id = create_model(model_raw, model_zip)
    return id


@model_router.get(
    "/{name}",
    response_model=GetModel,
    status_code=status.HTTP_200_OK,
)
async def get_model(name: str):
    return get_model_by_name(name)
