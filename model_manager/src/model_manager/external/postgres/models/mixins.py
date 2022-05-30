from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class TimestampMixin(object):
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now()
    )
    

class DictMixin(object):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
