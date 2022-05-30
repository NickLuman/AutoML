from datetime import datetime, timedelta

from pydantic import EmailStr

from ....settings import settings
from .models import CoreModel


class JWTMeta(CoreModel):
    token_issuer: str = settings.token_issuer
    token_intended_for: str
    token_issued_at: float = datetime.timestamp(datetime.utcnow())
    token_expires_in: float = datetime.timestamp(
        datetime.utcnow() + timedelta(seconds=settings.token_expires_in_secs)
    )


class JWTCredentials(CoreModel):
    username: str
    email: EmailStr


class JWTPayload(JWTMeta, JWTCredentials):
    pass


class AccessToken(CoreModel):
    access_token: str
    token_type: str
