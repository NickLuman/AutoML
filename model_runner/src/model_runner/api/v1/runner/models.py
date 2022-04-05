from pydantic import BaseModel


class ModelData(BaseModel):
    name: str
    params: dict


class Metadata(BaseModel):
    models: list[ModelData]
    target_column: str

