from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db import Base
from .mixins import DictMixin, TimestampMixin


class Model(Base, TimestampMixin, DictMixin):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    
    name = Column(String)
    description = Column(Text)

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="models")

    parameters = relationship("ModelParameter", back_populates="model", lazy=True)
    versions = relationship("ModelVersion", back_populates="model", lazy=True)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"Model(name={self.name})"
