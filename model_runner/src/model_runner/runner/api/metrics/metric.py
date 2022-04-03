from typing import Callable


class Metric:
    def __init__(self, name: str, calculate: Callable, best_when: str):
        self.name = name
        self.calculate = calculate
        self.best_when = best_when

        self.result_value = 0.0

    def calculate_result(self, test, prediction):
        self.result_value = self.calculate(test, prediction)

    def __repr__(self):
        return f"metric: {self.name}, result: {self.result_value}"
