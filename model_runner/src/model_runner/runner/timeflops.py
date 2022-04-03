from itertools import product
from operator import itemgetter

from api.models.dynamic_loader import DynamicLoader
from api.metrics.metrics_api import MetricsAPI
import matplotlib.pyplot as plt
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
        self, model, model_name: str, test_data, metrics_api: MetricsAPI, params: dict
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
            "model_name": model_name,
            "params": params,
            "metrics_value": {},
        }
        for metric in metrics_api.get_metrics():
            report["metrics_value"][metric.name] = metric.calculate(
                test_data[self.target], test_predictions
            )
        return report

    def _select_best_by_metric_result(self, reports: list) -> list:
        pass

    def search_best_models(
        self,
        data,
        target: str = "target",
        split_coef: float = 0.8,
        params_selection: bool = True,
        selection_metric: str = "",
    ):
        self.data = data
        self.target = target

        train, test = self._split_train_test(self.data, split_coef)

        metrics_api = MetricsAPI("all")
        best_reports = []

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

                report = self._evaluate_model(
                    model, model_name, test, metrics_api, prepared_params
                )

                if report:
                    reports.append(report)

                    self.models[model_name]["best_model"] = model

            best_report = max(
                reports, key=lambda x: x["metrics_value"][selection_metric]
            )
            best_reports.append(best_report)
        logger.info(best_reports)

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

    def plot_fitted_prediction(
        self,
    ):
        for model_name, _ in self.models.items():
            predictions = self.models[model_name]["current_model"].predict()
            plt.figure()
            plt.title(model_name)
            plt.plot(self.train_data, color="blue")
            plt.plot(predictions, color="red")
            plt.show()

    def forecast(
        self,
        steps: int = 1,
        best_model: bool = True,
        save_result: bool = False,
    ):
        pass
