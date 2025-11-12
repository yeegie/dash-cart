import logging
from .formatters import get_default_formatter
from .file_handler import get_file_handler


def get_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Консольный хендлер
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(get_default_formatter())
        logger.addHandler(stream_handler)

        # Файловый хендлер
        file_handler = get_file_handler()
        logger.addHandler(file_handler)

    return logger
