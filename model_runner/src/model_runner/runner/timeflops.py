from itertools import product
from copy import deepcopy

from api.models.dynamic_loader import DynamicLoader
from api.metrics.metrics_api import MetricsAPI
from loguru import logger


class TimeFlops:
    def __init__(self, models: dict):
        logger.info("TimeFlops pipeline initializing")

        self.models = models

    def _get_models(self, module_name: str, models: list[str]) -> dict:
        loader = DynamicLoader(module_name)
        models, not_founded_models = loader.search_models(models)

        for model_name, model_class in models.items():
            self.models[model_name]["class"] = model_class

        logger.warning(
            f"Impossible to find models with such names: {', '.join(not_founded_models)}"
        )

        self.models = dict((k, v) for k, v in self.models.items() if v.get("class"))

    def _split_train_test(self, data, split_coef: float) -> tuple:
        split_size = int(len(data) * split_coef)
        train, test = data.iloc[:split_size], data.iloc[split_size:]

        return (train, test)

    def _prepare_params(
        self, model_name: str, params: dict, params_selection: bool = False
    ) -> list:
        if not params:
            logger.error(f"No start params for initialize model {model_name}")
            return []

        params_set = [params]

        if params_selection:
            params_set = self.create_params_set(params=params)

        return params_set

    def _evaluate_model(
        self, model, test_data, metrics_api: MetricsAPI, params: dict
    ) -> dict:
        try:
            test_predictions = model.forecast(len(test_data))
        except AttributeError:
            logger.error(
                "Obtained model without 'forecast' method.\nImplement that method before use model!"
            )
        except Exception as exc:
            logger.error(exc)
            return {}

        report = {
            "params": params,
            "metrics": [],
        }
        for metric in metrics_api.get_metrics():
            current_metric = deepcopy(metric)
            current_metric.calculate_result(test_data[self.target], test_predictions)
            report["metrics"].append(current_metric)

        return report

    def _select_best_by_metric_result(self) -> list:
        pass

    def search_best_models(
        self,
        data,
        target: str = "target",
        split_coef: float = 0.8,
        params_selection: bool = True,
        evaluate_metrics: str = "all",
        selection_metric: str = "",
    ):
        self.data = data
        self.target = target

        train, test = self._split_train_test(self.data, split_coef)

        metrics_api = MetricsAPI(evaluate_metrics)

        if not selection_metric:
            logger.warning(
                "It'll be impossibe to select best model without selection metric"
            )

        self.best_reports = {}
        for model_name, model_data in self.models.items():
            model_class = model_data.get("class")
            model_params = model_data.get("params")

            model_params_set = self._prepare_params(
                model_name, model_params, params_selection
            )

            reports = []

            for params in model_params_set:
                prepared_params = dict(params) if params is not dict else params
                model = model_class(**prepared_params)

                model.fit(
                    train,
                    self.target,
                )
                self.models[model_name]["current_model"] = model

                report = self._evaluate_model(model, test, metrics_api, prepared_params)

                if report:
                    reports.append(report)

                    if selection_metric:
                        target_metric = next(
                            metr
                            for metr in report.get("metrics")
                            if metr.name == selection_metric
                        )
                        # TODO: report class
                        # TODO: separate logic
                        if not self.models[model_name].get("best_metric_val"):
                            self.models[model_name][
                                "best_metric_val"
                            ] = target_metric.result_value
                            self.models[model_name]["best_model"] = model
                            self.best_reports[model_name] = report
                            continue

                        if (
                            target_metric.best_when == "min"
                            and self.models[model_name]["best_metric_val"]
                            > target_metric.result_value
                        ) or (
                            target_metric.best_when == "max"
                            and self.models[model_name]["best_metric_val"]
                            < target_metric.result_value
                        ):
                            self.models[model_name]["best_model"] = model
                            self.best_reports[model_name] = report

    def get_best_reports(self) -> dict:
        return self.best_reports if self.best_reports else {}

    def create_params_set(
        self, minus_shift: int = 1, plus_shift: int = 1, **dict
    ) -> map:
        params_set = []
        params = dict.get("params", {})

        for _, param_base_val in params.items():
            if param_base_val - minus_shift < 0:
                minus_shift = param_base_val

            params_seq_list = list(
                range(param_base_val - minus_shift, param_base_val + plus_shift + 1)
            )

            params_set.append(params_seq_list)

        result_set = product(*params_set)
        result_set_dict = map(
            lambda x_set: zip(params.keys(), x_set),
            result_set,
        )
        return result_set_dict

    def forecast(
        self,
        model_name: str,
        steps: int = 1,
        best_model: bool = True,
    ):
        model_type = "best_model" if best_model else "current_model"
        return self.models[model_name][model_type].forecast(steps)
