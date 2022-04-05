from datetime import datetime

from pydantic import BaseModel

from ..models.models import Model
from ..modules.models import Module


class CreateProject(BaseModel):
    name: str
    description: str
    user_id: int
    created_at: datetime
    status: str

    class Config:
        orm_mode = True


class Project(BaseModel):
    id: int
    name: str
    description: str
    user_id: int
    created_at: datetime
    status: str
    models: list[Model]
    modules: list[Module]

    class Config:
        orm_mode = True
