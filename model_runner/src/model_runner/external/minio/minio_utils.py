import tempfile
import shutil
from zipimport import zipimporter

from minio import Minio

from .minio import minio_client
from ...runner.api.loaders.dynamic_loader import DynamicLoader
from ...settings import settings


def connect_to_minio():
    minio_client.minio = Minio(
        f"{settings.minio_host}:{settings.minio_port}",
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=False,
    )


def get_model(s3_bucket: str, module_name: str, class_name: str):
    tmp_dirpath = tempfile.mkdtemp()

    tmp_filename = s3_filename = f"{module_name}.zip"
    tmp_filepath = f"{tmp_dirpath}/{tmp_filename}"
    minio_client.minio.fget_object(s3_bucket, s3_filename, tmp_filepath)

    importer = zipimporter(tmp_filepath)
    module = importer.load_module(module_name)
    model_cls, _ = DynamicLoader.search_models(module, [class_name])

    shutil.rmtree(tmp_dirpath)

    if not model_cls:
        raise Exception("No such model in Minio object storage")

    return model_cls
