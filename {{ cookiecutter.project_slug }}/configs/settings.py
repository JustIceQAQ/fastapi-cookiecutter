import datetime
import os
from enum import Enum
from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import Field
from helpers.utils.datetime.helper import datetime_now


class DeployStatus(str, Enum):
    Local = "local"
    Development = "development"
    Production = "production"
    Test = "test"


class GenerallySettings(BaseSettings):
    ENVIRONMENT: str
    IS_DEBUG: bool
    ACCESS_CONTROL_ALLOW_ORIGIN: list | None = ["*"]
    RUNSERVER_DATETIME: datetime.datetime = Field(default_factory=datetime_now)

    FASTAPI_DOCS_URL: str | None = "/docs"
    FASTAPI_OPENAPI_URL: str | None = "/openapi.json"
    FASTAPI_REDOC_URL: str | None = "/redoc"


class LocalSettings(GenerallySettings):
    ENVIRONMENT: str = DeployStatus.Local
    IS_DEBUG: bool = True

    class Config:
        env_file = ".env/.local.env"
        env_file_encoding = "utf-8"


class DevelopmentSettings(GenerallySettings):
    ENVIRONMENT: str = DeployStatus.Development
    IS_DEBUG: bool = True

    class Config:
        env_file = ".env/.development.env"
        env_file_encoding = "utf-8"


class TestSettings(GenerallySettings):
    ENVIRONMENT: str = DeployStatus.Test
    IS_DEBUG: bool = True

    class Config:
        env_file = ".env/.test.env"
        env_file_encoding = "utf-8"


class ProductionSettings(GenerallySettings):
    ENVIRONMENT: str = DeployStatus.Production
    IS_DEBUG: bool = False

    class Config:
        env_file = ".env/.production.env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> GenerallySettings:
    deploy_status = os.getenv("ENVIRONMENT", default=DeployStatus.Local)

    if deploy_status in {DeployStatus.Local}:
        runtime_settings = LocalSettings()
    elif deploy_status in {DeployStatus.Development}:
        runtime_settings = DevelopmentSettings()
    elif deploy_status in {DeployStatus.Production}:
        runtime_settings = ProductionSettings()
    elif deploy_status in {DeployStatus.Test}:
        runtime_settings = TestSettings()
    else:
        raise RuntimeError("Your environment are error.")

    return runtime_settings
