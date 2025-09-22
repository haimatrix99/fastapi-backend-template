from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    host: str = Field(default="0.0.0.0", alias="APP_HOST")
    port: int = Field(default=8080, alias="APP_PORT")
    environment: str = Field(default="dev", alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")
    log_level: str = Field(default="info", alias="LOG_LEVEL")

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
