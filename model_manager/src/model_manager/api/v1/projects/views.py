from http import HTTPStatus

from fastapi import APIRouter, Cookie, Depends, Response, status
from sqlalchemy.orm import Session

from ....external.postgres.db_utils import get_db
from ..base.utils import check_jwt_token_validity
from ..users.authentication import AuthService
from .core import (
    create_new_project,
    delete_project_by_name,
    get_project_by_name,
    get_user_projects,
)
from .models import ProjectCreate, ProjectPublic

projects_router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


@projects_router.post(
    "/",
    response_model=ProjectPublic,
    name="projects:create-new-project",
    status_code=status.HTTP_201_CREATED,
)
async def create_new_project_view(
    new_project: ProjectCreate,
    session: str = Cookie(None),
    db: Session = Depends(get_db),
):
    check_jwt_token_validity(session)
    username = AuthService.get_usernameJWT(session)

    created_project = create_new_project(
        username=username,
        new_project=new_project,
        db=db,
    )

    return ProjectPublic(**created_project.dict())


@projects_router.get(
    "/{name}",
    response_model=ProjectPublic,
    name="projects:get-project",
    status_code=status.HTTP_200_OK,
)
async def get_project_view(
    name: str,
    session: str = Cookie(None),
    db: Session = Depends(get_db),
):
    check_jwt_token_validity(session)
    username = AuthService.get_usernameJWT(session)

    found_project = get_project_by_name(
        username=username,
        name=name,
        db=db,
    )

    return ProjectPublic(**found_project.dict())


@projects_router.get(
    "/",
    response_model=list[ProjectPublic],
    name="projects:get-all-projects",
    status_code=status.HTTP_200_OK,
)
async def get_all_projects_view(
    session: str = Cookie(None),
    db: Session = Depends(get_db),
):
    check_jwt_token_validity(session)
    username = AuthService.get_usernameJWT(session)

    found_projects = get_user_projects(
        username=username,
        db=db,
    )

    return [ProjectPublic(**project.dict()) for project in found_projects]


@projects_router.delete(
    "/{name}",
    name="projects:delete-project",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project_view(
    name: str,
    session: str = Cookie(None),
    db: Session = Depends(get_db),
):
    check_jwt_token_validity(session)
    username = AuthService.get_usernameJWT(session)

    delete_project_by_name(
        username=username,
        name=name,
        db=db,
    )

    return Response(status_code=HTTPStatus.NO_CONTENT.value)
