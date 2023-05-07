from typing import Literal
from pydantic import BaseSettings, SecretStr


class Config(BaseSettings):
    APP_HOST: str
    APP_PORT: str
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: SecretStr


def get_config() -> Config:
    return Config(_env_file=".env", _env_file_encoding="utf-8")
