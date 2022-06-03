from fastapi import APIRouter, Cookie, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from ....external.postgres.db_utils import get_db
from ..base.utils import check_jwt_token_validity
from ..users.authentication import AuthService
from .core import create_new_model_version
from .models import ModelVersionCreate, ModelVersionPublic

model_versions_router = APIRouter(
    prefix="/api/v1/model-versions", tags=["model-versions"]
)


@model_versions_router.post(
    "/{project_name}/{model_name}",
    response_model=ModelVersionPublic,
    name="model-versions:create-new-model-version",
    status_code=status.HTTP_201_CREATED,
)
async def create_new_model_version_view(
    project_name: str,
    model_name: str,
    new_model_version_raw: str = Form(...),
    new_model_version_zip: UploadFile = File(...),
    session: str = Cookie(None),
    db: Session = Depends(get_db),
):
    check_jwt_token_validity(session)
    username = AuthService.get_usernameJWT(session)

    created_model_version = create_new_model_version(
        username=username,
        project_name=project_name,
        model_name=model_name,
        new_model_version_raw=new_model_version_raw,
        new_model_version_zip=new_model_version_zip,
        db=db,
    )

    return ModelVersionPublic(**created_model_version.dict())
