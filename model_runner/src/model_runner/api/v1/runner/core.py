from datetime import datetime
from io import StringIO
from operator import mod
from uuid import uuid4

from fastapi import File
from loguru import logger
import pandas as pd

from ....runner.timeflops import TimeFlops
from ....external.minio.minio_utils import minio_client, get_model
from ....external.model_manager.requests import get_model_by_name
from .models import ModelData, Metadata


async def fit_best_models(
    metadata: Metadata,
    data_file: File,
):
    prepared_models = {}

    for model in metadata.models:
        model_data = await get_model_by_name(model.name)
        s3_bucket, module_name, class_name = (
            model_data.get("s3_bucket"),
            model_data.get("module_name"),
            model_data.get("class_name"),
        )
        model_cls = get_model(s3_bucket, module_name, class_name)
        prepared_models[model.name] = {}
        prepared_models[model.name]["class"] = model_cls[model.name]
        prepared_models[model.name]["params"] = model.params

    tf = TimeFlops(experiment_id=uuid4(), models=prepared_models)
    df = get_df(data_file)

    tf.search_best_models(df, metadata.target_column, selection_metric="R-2")
    logger.info(tf.get_best_reports())


def get_df(data_file: File):
    df = pd.read_csv(
        StringIO(str(data_file.file.read(), "utf-8")),
        header=0,
        parse_dates=[0],
        index_col=0,
        date_parser=lambda x: datetime.strptime(x, "%m/%d/%Y"),
        encoding="utf-8",
    )

    return df
