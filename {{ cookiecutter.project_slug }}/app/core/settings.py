from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    host: str = Field(default="0.0.0.0", alias="APP_HOST")
    port: int = Field(default=8080, alias="APP_PORT")
    environment: str = Field(default="dev", alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
{% if cookiecutter.include_database == "y" -%}

    # Database settings
    database_url: str = Field(default="{{ cookiecutter.database_url }}", alias="DATABASE_URL")
    database_type: str = Field(default="{{ cookiecutter.database_type }}", alias="DATABASE_TYPE")
{%- endif %}
{% if cookiecutter.include_redis == "y" -%}

    # Redis settings
    redis_enabled: bool = Field(default=True, alias="REDIS_ENABLED")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    redis_max_connections: int = Field(default=10, alias="REDIS_MAX_CONNECTIONS")
    redis_decode_responses: bool = Field(default=True, alias="REDIS_DECODE_RESPONSES")
    redis_socket_timeout: int = Field(default=5, alias="REDIS_SOCKET_TIMEOUT")
    redis_socket_connect_timeout: int = Field(default=5, alias="REDIS_SOCKET_CONNECT_TIMEOUT")
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