from typing import Optional

from pydantic import EmailStr, constr

from ..base.models.core import CoreModel, DateTimeModelMixin, IDModelMixin


class UserBase(CoreModel):
    username: Optional[str]
    email: Optional[EmailStr]

    firstname: str
    lastname: str

    is_email_verified: bool = False
    is_active: bool = True


class UserCreate(CoreModel):
    username: constr(min_length=6, max_length=16, regex="^[a-zA-Z0-9_-]+$")
    email: EmailStr
    password: constr(
        min_length=8,
        max_length=128,
        regex="^[a-zA-Z0-9~!@#$%^&*='|:\". <>,.? /]+$",
    )


class UserEnter(CoreModel):
    username: str
    password: str


class UserLogin(CoreModel):
    username: str


class UserUpdate(CoreModel):
    firstname: constr(
        min_length=1,
        max_length=64,
        regex="^[a-zA-ZА-я\-]+$",
    )
    lastname: constr(
        min_length=1,
        max_length=64,
        regex="^[a-zA-ZА-я\-]+$",
    )


class UserUpdatePublic(CoreModel):
    username: str

    firstname: str
    lastname: str

    class Config:
        orm_mode = True


class UserPublicEnter(CoreModel):
    username: str
    email: EmailStr


class UserPasswordUpdate(CoreModel):
    password: constr(
        min_length=8,
        max_length=128,
        regex="^[a-zA-Z0-9~!@#$%^&*='|:\". <>,.? /]+$",
    )
    salt: str


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    password: constr(
        min_length=8,
        max_length=128,
        regex="^[a-zA-Z0-9~!@#$%^&*='|:\". <>,.? /]+$",
    )
    salt: str

    class Config:
        orm_mode = True


class UserPublic(IDModelMixin, DateTimeModelMixin, UserBase):
    class Config:
        orm_mode = True
