from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base
from .mixins import DictMixin


class InformationCriterion(Base, DictMixin):
    __tablename__ = "information_criteria"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    value = Column(Float, default=0.0)

    model_id = Column(Integer, ForeignKey("model_versions.id"))
    model = relationship("ModelVersion", back_populates="information_criteria")

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"InformationCriterion(model_version.name={self.model_version.name}, name={self.name}, value={self.value})"
