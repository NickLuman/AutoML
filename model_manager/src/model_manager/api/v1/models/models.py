from pydantic import BaseModel


class CreateModel(BaseModel):
    name: str
    description: str
    user_id: int
    s3_bucket: str
    module_name: str
    class_name: str
    project_id: int

    class Config:
        orm_mode = True


class Model(BaseModel):
    id: int
    name: str
    description: str
    user_id: int
    s3_bucket: str
    module_name: str
    class_name: str
    project_id: int

    class Config:
        orm_mode = True
