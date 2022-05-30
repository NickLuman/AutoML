from sqlalchemy import Column, ForeignKey, Integer, Table

from ..db import Base

users_roles = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
)
