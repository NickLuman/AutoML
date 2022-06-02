from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.orm import Session

from ....external.postgres.models.project import Project
from ..base.utils import get_user_by_username as get_user_db
from .models import ProjectCreate, ProjectGet, ProjectInDB


def create_new_project(
    *, username: str, new_project: ProjectCreate, db: Session
) -> ProjectInDB:
    user_record = get_user_db(
        username=username,
        db=db,
    )

    db_project = (
        db.query(Project)
        .with_parent(user_record)
        .filter(Project.name == new_project.name)
        .first()
    )

    if db_project:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project with such name already exists",
        )

    project = None

    try:
        addtional_data = {"user_id": user_record.id}

        updated_project_params = new_project.copy(update=addtional_data)

        created_project = Project(**updated_project_params.dict())
        db.add(created_project)

        db.flush()

        project = ProjectInDB(**created_project.__dict__)

        db.commit()

    except Exception as exc:
        logger.error(exc)

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project isn't created",
        )

    return project


def get_project_by_name(*, username: str, name: str, db: Session) -> ProjectInDB:
    user_record = get_user_db(
        username=username,
        db=db,
    )

    db_project = (
        db.query(Project).with_parent(user_record).filter(Project.name == name).first()
    )

    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project with such name name doesn't exist",
        )

    return ProjectInDB(**db_project.__dict__)


def get_user_projects(*, username: str, db: Session) -> list[ProjectInDB]:
    user_record = get_user_db(
        username=username,
        db=db,
    )

    db_projects = db.query(Project).with_parent(user_record).all()

    if not db_projects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't have any projects",
        )

    result_projects = [ProjectInDB(**project.__dict__) for project in db_projects]

    return result_projects


def delete_project_by_name(*, username: str, name: str, db: Session) -> int:
    user_record = get_user_db(
        username=username,
        db=db,
    )

    db.query(Project).with_parent(user_record).filter(Project.name == name).delete(
        synchronize_session=False
    )

    db.commit()
