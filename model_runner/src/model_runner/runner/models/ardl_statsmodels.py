from pandas import DataFrame
from statsmodels.tsa.api import ARDL
from loguru import logger


class ArDLStatsModels:
    def __init__(self, lags: int):
        logger.info("Initialising ArDL object")

        self.lags = lags

        self.ardl_model = ARDL
        self.model = None

    def fit(self, df: DataFrame, target_column: str = ""):

        target_train_series = df[target_column]

        self.untrained_model = self.ardl_model(
            target_train_series,
            self.lags,
        )
        self.model = self.untrained_model.fit()

    def predict(self):
        return self.model.predict()

    def forecast(self, steps: int = 1):
        return self.model.forecast(steps)

    def get_model_summary(self):
        return self.model.summary()
