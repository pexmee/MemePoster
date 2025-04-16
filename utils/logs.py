import logging

import colorlog

DATE_FMT = "%Y-%m-%d %H:%M:%S"
logger = logging.getLogger("pansophical_memes")


def setup_logger(
    name: str = "pansophical_memes",
    log_file: str = "logs.txt",
    level: int = logging.DEBUG,
):

    # Logger
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(level)

        # Stream handler
        handler = logging.StreamHandler()
        handler.setLevel(level)

        formatter = colorlog.ColoredFormatter(
            fmt="%(log_color)s%(asctime)s|%(name)s|%(levelname)s| [%(prefix)s] | %(message)s",
            datefmt=DATE_FMT,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt=DATE_FMT,
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger
