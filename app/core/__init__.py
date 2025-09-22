"""Core for fastapi-backend-template."""

from .logger import LOGGING_CONFIG
from .settings import get_settings

__all__ = ["get_settings", "LOGGING_CONFIG"]
