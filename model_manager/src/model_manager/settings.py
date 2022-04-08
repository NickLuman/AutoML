from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    minio_host: str
    minio_port: int
    minio_access_key: str
    minio_secret_key: str

    model_runner_host: str
    model_runner_port: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
