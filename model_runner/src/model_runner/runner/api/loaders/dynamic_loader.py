import importlib
import inspect

from loguru import logger


class DynamicLoader:
    def __init__(self, module_name: str):
        logger.info("Start dynamic model loading")

        self.module_name = module_name

        if importlib.util.find_spec(self.module_name) is not None:
            logger.info(f"{self.module_name} found, start module load")
        else:
            logger.error(f"cannot find the {self.module_name} module")
            raise ModuleNotFoundError

    def get_module(self):
        return importlib.import_module(self.module_name)

    @staticmethod
    def search_models(module, models_names: list[str]):
        class_in_module = inspect.getmembers(module, inspect.isclass)

        desired_class_set = set(models_names)

        target_classes = {}

        for class_name, class_ in class_in_module:
            if class_name in desired_class_set:
                target_classes[class_name] = class_
                desired_class_set.remove(class_name)

        not_founded_models = list(desired_class_set)

        return target_classes, not_founded_models
