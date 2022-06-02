from typing import Optional

from pydantic import constr

from ....external.postgres.models.project import ProjectStatus
from ..base.models.core import CoreModel, DateTimeModelMixin


class ProjectBase(CoreModel):
    name: Optional[str]
    description: Optional[str]

    status: Optional[ProjectStatus]


class ProjectCreate(CoreModel):
    name: constr(min_length=4, max_length=128)
    description: str

    status: ProjectStatus


class ProjectInDB(DateTimeModelMixin, ProjectBase):
    user_id: str

    class Config:
        orm_mode = True


class ProjectPublic(DateTimeModelMixin, ProjectBase):
    class Config:
        orm_mode = True


class ProjectGet(CoreModel):
    name: str


# class CreateProject(BaseModel):
#     name: str
#     description: str
#     created_at: datetime
#     status: str

#     class Config:
#         orm_mode = True


# class Project(BaseModel):
#     id: int
#     name: str
#     description: str
#     user_id: int
#     created_at: datetime
#     status: str
#     models: list[Model]
#     modules: list[Module]

#     class Config:
#         orm_mode = True
