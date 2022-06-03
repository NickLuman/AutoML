from fastapi import APIRouter, Cookie, Depends, status
from sqlalchemy.orm import Session

from ....external.postgres.db_utils import get_db
from ..base.utils import check_jwt_token_validity
from ..users.authentication import AuthService
from .core import create_new_model
from .models import ModelCreate, ModelPublic

models_router = APIRouter(prefix="/api/v1/models", tags=["models"])


@models_router.post(
    "/{project_name}",
    response_model=ModelPublic,
    name="models:create-new-model",
    status_code=status.HTTP_201_CREATED,
)
async def create_new_model_view(
    project_name: str,
    new_model: ModelCreate,
    session: str = Cookie(None),
    db: Session = Depends(get_db),
):
    check_jwt_token_validity(session)
    username = AuthService.get_usernameJWT(session)

    created_model = create_new_model(
        username=username,
        project_name=project_name,
        new_model=new_model,
        db=db,
    )

    return ModelPublic(**created_model.dict())
