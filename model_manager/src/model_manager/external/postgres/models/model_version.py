from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db import Base
from .mixins import DictMixin, TimestampMixin


class ModelVersion(Base, TimestampMixin, DictMixin):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    description = Column(Text)

    s3_bucket = Column(String, nullable=False)
    module_name = Column(String, nullable=False)
    class_name = Column(String, nullable=False)

    model_id = Column(Integer, ForeignKey("models.id"))
    model = relationship("Model", back_populates="versions")

    metrics = relationship("Metric", back_populates="model", lazy=True)
    information_criteria = relationship("InformationCriterion", back_populates="model", lazy=True)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"ModelVersion(model.name={self.model.name}, name={self.name})"
