from fastapi_sqlalchemy import db

from fastapi import HTTPException
from ....external.postgres.models import Project as DB_Project
from .models import CreateProject


def create_project(project: CreateProject) -> int:
    db_project = DB_Project(
        name=project.name,
        description=project.description,
        user_id=project.user_id,
        created_at=project.created_at,
        status=project.status,
    )

    db.session.add(db_project)
    db.session.commit()

    return db_project.id


def get_project_by_id(id_: int):
    project = db.session.query(DB_Project).get({"id": id_})

    if not project:
        raise HTTPException(status_code=404, detail="No project with such id")

    return project
