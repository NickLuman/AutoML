import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db import Base
from .mixins import DictMixin, TimestampMixin


class ProjectStatus(enum.Enum):
    active = enum.auto()
    frozen = enum.auto()
    deprecated = enum.auto()
    closed = enum.auto()


class Project(Base, TimestampMixin, DictMixin):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)

    name = Column(String, primary_key=True, index=True)
    description = Column(Text)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="projects")

    status = Column(Enum(ProjectStatus))

    modules = relationship("Module", back_populates="project", lazy=True)
    models = relationship("Model", back_populates="project", lazy=True)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"Project(name={self.name}, user.username={self.user.username})"
