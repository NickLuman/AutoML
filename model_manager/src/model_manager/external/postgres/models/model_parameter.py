from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base
from .mixins import DictMixin


class ModelParameter(Base, DictMixin):
    __tablename__ = "model_parameters"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    data_type = Column(String)    
    value = Column(String)

    model_id = Column(Integer, ForeignKey("models.id"))
    model = relationship("Model", back_populates="parameters")

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"ModelParameter(name={self.name}, data_type={self.data_type})"
