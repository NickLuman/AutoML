from minio import Minio

from .minio import minio_client
from ...settings import settings


def connect_to_minio():
    minio_client.minio = Minio(
        f"{settings.minio_host}:{settings.minio_port}",
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=False,
    )
