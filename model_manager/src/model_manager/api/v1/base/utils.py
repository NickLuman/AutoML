from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ....external.postgres.models.model import Model
from ....external.postgres.models.project import Project
from ....external.postgres.models.user import User
from ..users.authentication import JWTBearer


def get_user_by_username(*, username: str, db: Session) -> User:
    user_record = db.query(User).filter(User.username == username).first()

    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such user"
        )

    return user_record


def get_user_project_by_name(*, user: User, name: str, db: Session) -> Project:
    project_record = (
        db.query(Project).with_parent(user).filter(Project.name == name).first()
    )

    if not project_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such project",
        )

    return project_record


def get_project_model_by_name(
    *, user: User, project_name: str, name: str, db: Session
) -> Model:
    project = get_user_project_by_name(user=user, name=project_name, db=db)

    model_record = (
        db.query(Model).with_parent(project).filter(Model.name == name).first()
    )

    if not model_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such model",
        )

    return model_record


def check_jwt_token_validity(session):
    if not JWTBearer.verify_jwt(session):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
