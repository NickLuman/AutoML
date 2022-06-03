from fastapi import APIRouter, Body, Cookie, Depends, Response, status
from sqlalchemy.orm import Session

from ....external.postgres.db_utils import get_db
from ....settings import settings
from ..base.utils import check_jwt_token_validity
from .authentication import AuthService
from .core import (
    auth_service,
    authenticate_user,
    get_user,
    register_new_user,
    update_user_data,
)
from .models import (
    UserCreate,
    UserEnter,
    UserLogin,
    UserPublic,
    UserPublicEnter,
    UserUpdate,
    UserUpdatePublic,
)
from .token import AccessToken

users_router = APIRouter(prefix="/api/v1/users", tags=["users"])


@users_router.post(
    "/register",
    response_model=UserPublic,
    name="user:register-new-user",
    status_code=status.HTTP_201_CREATED,
)
async def register_new_user_view(
    response: Response,
    new_user: UserCreate = Body(...),
    db: Session = Depends(get_db),
):
    created_user = register_new_user(new_user=new_user, db=db)

    access_token = AccessToken(
        access_token=auth_service.create_access_token(user=created_user),
        token_type="Bearer",
    )

    cookie = access_token.access_token

    response.set_cookie(
        key="session",
        value=cookie,
        max_age=settings.token_expires_in_secs,
        httponly=True,
    )

    return UserPublic(**created_user.dict())


@users_router.get(
    "/",
    response_model=UserPublicEnter,
    name="user:get-user",
    status_code=status.HTTP_200_OK,
)
async def get_user_view(
    response: Response,
    session: str = Cookie(None),
    db: Session = Depends(get_db),
):
    check_jwt_token_validity(session)

    username = AuthService.get_usernameJWT(session)

    user = get_user(username=username, db=db)

    access_token = AccessToken(
        access_token=auth_service.create_access_token(user=user),
        token_type="bearer",
    )

    cookie = access_token.access_token

    response.set_cookie(
        key="session",
        value=cookie,
        max_age=settings.token_expires_in_secs,
        httponly=True,
    )

    return UserPublicEnter(username=user.username, email=user.email)


@users_router.post(
    "/login/token",
    name="user:login-and-password",
)
async def user_login_with_usernames_and_password(
    response: Response,
    db: Session = Depends(get_db),
    form_data: UserEnter = Body(...),
) -> str:
    user = authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=db,
    )

    access_token = AccessToken(
        access_token=auth_service.create_access_token(user=user),
        token_type="bearer",
    )

    cookie = access_token.access_token

    response.set_cookie(
        key="session",
        value=cookie,
        max_age=settings.token_expires_in_secs,
        httponly=True,
    )

    return UserLogin(**user.dict())


@users_router.put(
    "/",
    response_model=UserUpdatePublic,
    name="user:update-user",
    status_code=status.HTTP_201_CREATED,
)
async def update_user_data_view(
    session: str = Cookie(None),
    update_data: UserUpdate = Body(...),
    db: Session = Depends(get_db),
):
    check_jwt_token_validity(session)
    username = AuthService.get_usernameJWT(session)

    user_update_data = update_user_data(
        username=username,
        update_data=update_data,
        db=db,
    )

    return UserUpdatePublic(**user_update_data.dict())
