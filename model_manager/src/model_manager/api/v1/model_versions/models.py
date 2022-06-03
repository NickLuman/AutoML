from typing import Optional

from pydantic import constr

from ..base.models.core import CoreModel, DateTimeModelMixin


class ModelVersionBase(CoreModel):
    name: Optional[str]
    description: Optional[str]

    s3_bucket: Optional[str]
    module_name: Optional[str]
    class_name: Optional[str]


class ModelVersionCreate(CoreModel):
    name: constr(min_length=4, max_length=128)
    description: str

    s3_bucket: str
    module_name: str
    class_name: str


class ModelVersionInDB(DateTimeModelMixin, ModelVersionBase):
    model_id: str

    class Config:
        orm_mode = True


class ModelVersionPublic(DateTimeModelMixin, ModelVersionBase):
    class Config:
        orm_mode = True
