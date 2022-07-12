from pydantic import BaseSettings


class Settings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str
    bucket_name: str
    folder_name: str

    class Config:
        env_file = ".env"