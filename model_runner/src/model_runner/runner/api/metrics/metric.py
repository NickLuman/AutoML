from typing import Callable


class Metric:
    def __init__(self, name: str, calculate: Callable, best_when: str):
        self.name = name
        self.calculate = calculate
        self.best_when = best_when
