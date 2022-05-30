from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base
from .users_roles import users_roles


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String,  unique=True, nullable=False, index=True)

    users = relationship("User", secondary=users_roles, back_populates="roles")

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self): 
        return f"Role(name={self.name})"
