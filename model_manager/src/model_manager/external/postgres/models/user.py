from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base
from .mixins import DictMixin, TimestampMixin
from .users_roles import users_roles


class User(Base, TimestampMixin, DictMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String, unique=True, nullable=False, index=True)

    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)

    email = Column(String, unique=True, nullable=False, index=True)

    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)

    is_email_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    roles = relationship("Role", secondary=users_roles, back_populates="users")
    projects = relationship("Project", back_populates="user", lazy=True)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"
