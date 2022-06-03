from typing import Optional

from pydantic import constr

from ..base.models.core import CoreModel, DateTimeModelMixin


class ModelBase(CoreModel):
    name: Optional[str]
    description: Optional[str]


class ModelCreate(CoreModel):
    name: constr(min_length=4, max_length=128)
    description: str


class ModelInDB(DateTimeModelMixin, ModelBase):
    project_id: str

    class Config:
        orm_mode = True


class ModelPublic(DateTimeModelMixin, ModelBase):
    class Config:
        orm_mode = True
