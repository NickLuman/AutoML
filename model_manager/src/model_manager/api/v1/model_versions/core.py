import shutil
import tempfile

from fastapi import HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from loguru import logger
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ....external.minio.minio import minio_client
from ....external.postgres.models.model_version import ModelVersion
from ..base.utils import get_project_model_by_name as get_model_db
from ..base.utils import get_user_by_username as get_user_db
from .models import ModelVersionCreate, ModelVersionInDB


def create_new_model_version(
    *,
    username: str,
    project_name: str,
    model_name: str,
    new_model_version_raw: str,
    new_model_version_zip: UploadFile,
    db: Session,
) -> ModelVersionInDB:
    try:
        new_model_version = ModelVersionCreate.parse_raw(new_model_version_raw)
    except ValidationError as exc:
        logger.error(exc)

        raise HTTPException(
            detail=jsonable_encoder(exc.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        ) from exc

    user_record = get_user_db(
        username=username,
        db=db,
    )

    model_record = get_model_db(
        user=user_record, project_name=project_name, name=model_name, db=db
    )

    db_model_version = (
        db.query(ModelVersion)
        .with_parent(model_record)
        .filter(ModelVersion.name == new_model_version.name)
        .first()
    )

    if db_model_version:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Model Version with such name already exists",
        )

    tmp_dirpath = tempfile.mkdtemp()
    model_version = None

    try:
        addtional_data = {"model_id": model_record.id}

        updated_model_version_params = new_model_version.copy(update=addtional_data)

        created_model_verison = ModelVersion(**updated_model_version_params.dict())
        db.add(created_model_verison)

        db.flush()

        model_version = ModelVersionInDB(**created_model_verison.__dict__)

        tmp_filepath = f"{tmp_dirpath}/{model_version.module_name}"
        with open(tmp_filepath, "wb") as buffer:
            shutil.copyfileobj(new_model_version_zip.file, buffer)

        is_bucket_exists = minio_client.minio.bucket_exists(model_version.s3_bucket)

        if not is_bucket_exists:
            minio_client.minio.make_bucket(model_version.s3_bucket)

        minio_client.minio.fput_object(
            model_version.s3_bucket, f"{model_version.module_name}.zip", tmp_filepath
        )

        db.commit()
    except Exception as exc:
        logger.error(exc)

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model Version isn't created",
        )
    finally:
        shutil.rmtree(tmp_dirpath)

    return model_version
