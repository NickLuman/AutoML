from typing import Union

import numpy as np
from sklearn.metrics import r2_score, mean_squared_error
from loguru import logger

from .metric import Metric


class MetricsAPI:
    def __init__(self, target_metrics: Union[str, list[str]]):
        """
        R-2 - R-Squared
        MAPE - Mean Absolute Percentage Error
        RMSE - Root Mean Squared Error
        WAPE - Weighted Absolute Percentage Error
        """
        self.metrics = [
            Metric("R-2", r2_score, "max"),
            Metric("MAPE", self._mean_absolute_percentage_error, "min"),
            Metric("RMSE", mean_squared_error, "min"),
            Metric("WAPE", self._weighted_absolute_percentage_error, "min"),
        ]
        self.target_metrics = target_metrics

    def get_metrics(self) -> list:
        if self.target_metrics == "all":
            return self.metrics

        available_metrics = set([metr.name for metr in self.metrics])
        result_metrics = []

        for metric in self.target_metrics:
            if metric not in available_metrics:
                logger.error(f"No such metric {metric}")
            result_metrics.append(
                next(metr for metr in self.metrics if metr.name == metric)
            )

        return result_metrics

    def _mean_absolute_percentage_error(self, y_true, y_pred) -> float:
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    def _weighted_absolute_percentage_error(self, y_true, y_pred) -> float:
        return ((y_true - y_pred).abs().sum() / y_true.abs().sum()) * 100
