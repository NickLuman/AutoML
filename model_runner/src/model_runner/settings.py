from pydantic import BaseSettings


class Settings(BaseSettings):
    minio_host: str
    minio_port: int
    minio_access_key: str
    minio_secret_key: str

    model_manager_host: str
    model_manager_port: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
