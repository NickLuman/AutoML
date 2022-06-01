from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ....external.postgres.models.user import User
from ..users.authentication import JWTBearer


def get_user_by_username(*, username: str, db: Session) -> User:
    user_record = db.query(User).filter(User.username == username).first()

    if not user_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such user")

    return user_record


def check_jwt_token_validity(session):
    if not JWTBearer.verify_jwt(session):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
