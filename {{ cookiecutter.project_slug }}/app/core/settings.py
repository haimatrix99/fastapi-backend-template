from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    host: str = Field(default="{{ cookiecutter.app_host }}", alias="APP_HOST")
    port: int = Field(default={{ cookiecutter.app_port }}, alias="APP_PORT")
    environment: str = Field(default="dev", alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
{% if cookiecutter.include_database == "y" -%}

    # Database settings
    database_url: str = Field(default="{{ cookiecutter.database_url }}", alias="DATABASE_URL")
    database_type: str = Field(default="{{ cookiecutter.database_type }}", alias="DATABASE_TYPE")
{%- endif %}

    @field_validator("log_level", mode="before")
    @classmethod
    def validate_log_level(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v

    @property
    def reload(self):
        return self.environment == "dev"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()