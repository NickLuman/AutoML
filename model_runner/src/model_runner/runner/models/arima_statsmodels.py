from pandas import DataFrame
from statsmodels.tsa.arima.model import ARIMA
from loguru import logger


class ARIMAStatsModels:
    def __init__(self, q: int, d: int, p: int):
        logger.info("Initialising ARIMA object")

        self.p = p
        self.q = q
        self.d = d

        self.arima_model = ARIMA
        self.model = None

    def fit(self, df: DataFrame, target_column: str = ""):
        order = (self.p, self.d, self.q)

        target_train_series = df[target_column]

        self.untrained_model = self.arima_model(
            target_train_series,
            order=order,
        )
        self.model = self.untrained_model.fit()

    def predict(self):
        return self.model.predict()

    def forecast(self, steps: int = 1):
        return self.model.forecast(steps)

    def get_model_summary(self):
        return self.model.summary()
