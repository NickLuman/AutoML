from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base
from .mixins import DictMixin, TimestampMixin


class Module(Base, TimestampMixin, DictMixin):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    version = Column(String)

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="modules")

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"Module(name={self.name}, version={self.version})"
