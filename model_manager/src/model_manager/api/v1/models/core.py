from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.orm import Session

from ....external.postgres.models.model import Model
from ..base.utils import get_user_by_username as get_user_db
from ..base.utils import get_user_project_by_name as get_project_db
from .models import ModelCreate, ModelInDB


def create_new_model(
    *, username: str, project_name: str, new_model: ModelCreate, db: Session
) -> ModelInDB:
    user_record = get_user_db(
        username=username,
        db=db,
    )

    project_record = get_project_db(user=user_record, name=project_name, db=db)

    db_model = (
        db.query(Model)
        .with_parent(project_record)
        .filter(Model.name == new_model.name)
        .first()
    )

    if db_model:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Model with such name already exists",
        )

    model = None

    try:
        addtional_data = {"project_id": project_record.id}

        updated_model_params = new_model.copy(update=addtional_data)

        created_model = Model(**updated_model_params.dict())
        db.add(created_model)

        db.flush()

        model = ModelInDB(**created_model.__dict__)

        db.commit()

    except Exception as exc:
        logger.error(exc)

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model isn't created",
        )

    return model
