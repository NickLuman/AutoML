import tempfile
import shutil

from fastapi_sqlalchemy import db
from fastapi import HTTPException, status, UploadFile
from fastapi.encoders import jsonable_encoder
from loguru import logger
from pydantic import ValidationError

from ....external.minio.minio import minio_client
from ....external.postgres.models import Model as DB_Model
from .models import CreateModel


def create_model(model_raw: str, model_zip: UploadFile) -> int:
    try:
        model = CreateModel.parse_raw(model_raw)
    except ValidationError as exc:
        raise HTTPException(
            detail=jsonable_encoder(exc.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        ) from exc

    tmp_dirpath = tempfile.mkdtemp()

    try:
        db_model = DB_Model(
            name=model.name,
            description=model.description,
            user_id=model.user_id,
            s3_bucket=model.s3_bucket,
            module_name=model.module_name,
            class_name=model.class_name,
            project_id=model.project_id,
        )

        db.session.add(db_model)
        db.session.commit()

        tmp_filepath = f"{tmp_dirpath}/{db_model.module_name}"
        with open(tmp_filepath, "wb") as buffer:
            shutil.copyfileobj(model_zip.file, buffer)

        is_bucket_exists = minio_client.minio.bucket_exists(db_model.s3_bucket)

        if not is_bucket_exists:
            minio_client.minio.make_bucket(db_model.s3_bucket)

        minio_client.minio.fput_object(
            db_model.s3_bucket, f"{db_model.module_name}.zip", tmp_filepath
        )
    except Exception as exc:
        logger.error(exc)
        db.session.rollback()

        raise HTTPException(
            detail=f"impossible to save model {model.name}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    finally:
        shutil.rmtree(tmp_dirpath)


def get_model_by_name(name: str):
    model = db.session.query(DB_Model).filter(DB_Model.name == name).first()

    return model
