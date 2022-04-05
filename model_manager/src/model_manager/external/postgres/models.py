from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String)

    models = relationship("Model", backref="project", lazy=True)
    modules = relationship("Module", backref="project", lazy=True)


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    user_id = Column(Integer, nullable=False)
    s3_bucket = Column(String, nullable=False)
    module_name = Column(String, nullable=False)
    class_name = Column(String, nullable=False)

    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)


class Module(Base):
    __tablename__ = "module"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    upload_at = Column(DateTime(timezone=True), server_default=func.now())
    version = Column(String)

    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)


class Parameter(Base):
    __tablename__ = "parameter"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    data_type = Column(String)
    value = Column(String)
