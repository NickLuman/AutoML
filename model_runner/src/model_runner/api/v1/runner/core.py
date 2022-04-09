from datetime import datetime
from io import StringIO
from uuid import uuid4

from fastapi import File
import pandas as pd

from ....runner.timeflops import TimeFlops
from ....external.minio.minio_utils import get_model
from ....external.model_manager.requests import get_model_by_name
from .models import (
    Metadata,
    BestReports,
    Metric,
    ModelData,
    Report,
)


async def fit_best_models(
    metadata: Metadata,
    data_file: File,
) -> BestReports:
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

    experiment_id = uuid4()

    tf = TimeFlops(experiment_id, models=prepared_models)
    df = _get_df(data_file)

    tf.search_best_models(
        df,
        target=metadata.target_column,
        split_coef=metadata.split_coef,
        selection_metric=metadata.selection_metric,
        params_selection=metadata.params_selection,
        evaluate_metrics=metadata.evaluate_metrics,
        minus_shift=metadata.minus_shift,
        plus_shift=metadata.plus_shift,
    )

    best_reports = tf.get_best_reports()

    return _map_best_reports(str(experiment_id), best_reports)


def _get_df(data_file: File):
    df = pd.read_csv(
        StringIO(str(data_file.file.read(), "utf-8")),
        header=0,
        parse_dates=[0],
        index_col=0,
        date_parser=lambda x: datetime.strptime(x, "%m/%d/%Y"),
        encoding="utf-8",
    )

    return df


def _map_best_reports(experiment_id: str, reports: dict) -> BestReports:
    best_reports = BestReports(experiment_id=experiment_id)
    prepared_reports = []

    for model_name, data in reports.items():
        model_params = data.get("params", {})
        model_data = ModelData(name=model_name, params=model_params)

        metrics = []
        for metric in data.get("metrics", ""):
            report_metric = Metric(name=metric.name, value=metric.result_value)
            metrics.append(report_metric)

        model_ics = data.get("ics", {})

        report = Report(model_data=model_data, metrics=metrics, ics=model_ics)
        prepared_reports.append(report)

    best_reports.reports = prepared_reports

    return best_reports
