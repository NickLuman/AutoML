from datetime import datetime

from pydantic import BaseModel


class Module(BaseModel):
    id: int
    name: str
    upload_at: datetime
    version: str

    class Config:
        orm_mode = True
