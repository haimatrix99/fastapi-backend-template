import logging
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Colored log formatter."""

    def __init__(
        self,
        fmt=None,
        datefmt=None,
        style="%",
        validate=True,
        colored: Optional[bool] = None,
    ):
        super().__init__(fmt, datefmt, style, validate)

        # ANSI color codes
        self.COLORS = {
            "DEBUG": "\033[36m",  # Cyan
            "INFO": "\033[32m",  # Green
            "WARNING": "\033[33m",  # Yellow
            "ERROR": "\033[31m",  # Red
            "CRITICAL": "\033[35m",  # Magenta
        }
        self.RESET = "\033[0m"  # Reset to default color

    def format(self, record):
        # Add color to the levelname
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"

        # Add color to the message based on level
        if record.levelno == logging.DEBUG:
            record.msg = f"{self.COLORS['DEBUG']}{record.msg}{self.RESET}"
        elif record.levelno == logging.INFO:
            record.msg = f"{self.COLORS['INFO']}{record.msg}{self.RESET}"
        elif record.levelno == logging.WARNING:
            record.msg = f"{self.COLORS['WARNING']}{record.msg}{self.RESET}"
        elif record.levelno == logging.ERROR:
            record.msg = f"{self.COLORS['ERROR']}{record.msg}{self.RESET}"
        elif record.levelno == logging.CRITICAL:
            record.msg = f"{self.COLORS['CRITICAL']}{record.msg}{self.RESET}"

        formatted_message = super().format(record)

        record.levelname = levelname

        return formatted_message


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "colored": {
            "()": "app.core.logger.ColoredFormatter",
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "root": {"handlers": ["default"]},
    "handlers": {
        "default": {
            "formatter": "colored",
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["default"],
            "level": "INFO",  # Logs INFO and above
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "INFO",  # Logs INFO and above
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["default"],
            "level": "INFO",  # Logs ERROR and above
            "propagate": False,
        },
    },
}
