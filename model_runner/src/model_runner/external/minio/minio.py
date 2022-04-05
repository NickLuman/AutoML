from typing import Optional
from minio import Minio


class MinioClient:
    minio: Optional[Minio]


minio_client = MinioClient()


def get_s3():
    return minio_client
