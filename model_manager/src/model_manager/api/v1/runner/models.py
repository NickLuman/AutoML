from typing import Union, Optional

from pydantic import BaseModel


class ModelData(BaseModel):
    name: str
    params: dict


class Metadata(BaseModel):
    models: list[ModelData]
    target_column: str
    split_coef: float
    evaluate_metrics: Union[str, list[str]]
    selection_metric: str
    params_selection: bool
    minus_shift: int
    plus_shift: int


class Metric(BaseModel):
    name: str
    value: float


class Report(BaseModel):
    model_data: ModelData
    metrics: list[Metric]


class BestReports(BaseModel):
    experiment_id: str
    reports: Optional[list[Report]]
