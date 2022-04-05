from fastapi import APIRouter

from .core import create_project, get_project_by_id
from .models import CreateProject, Project

project_router = APIRouter(prefix="/project", tags=["project"])


@project_router.post(
    "/",
    response_model=int,
    status_code=201,
)
async def add_project(project: CreateProject):
    id = create_project(project)
    return id


@project_router.get(
    "/{id}",
    response_model=Project,
    status_code=200,
)
async def get_project(id: int):
    project = get_project_by_id(id)

    return project
