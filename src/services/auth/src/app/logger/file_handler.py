import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from .formatters import get_default_formatter

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def get_file_handler(filename="app.log") -> logging.Handler:
    log_path = LOG_DIR / filename

    handler = RotatingFileHandler(
        log_path,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=5,             # хранить 5 старых файлов
        encoding="utf-8"
    )
    handler.setFormatter(get_default_formatter())
    return handler
