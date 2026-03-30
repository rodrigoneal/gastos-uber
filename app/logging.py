from sys import stdout

from loguru import logger as loguru_logger


def get_logger():
    loguru_logger.remove()

    # Arquivo
    loguru_logger.add(
        "logs.log",
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level} | "
            "{module}.{function}:{line} | "
            "{message}"
        ),
        level="INFO",
        colorize=False,
    )

    # Console
    loguru_logger.add(
        stdout,
        format=(
            "<green>{time:DD-MM-YYYY HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<magenta>{module}</magenta>."
            "<blue>{function}</blue>"
            "<yellow>:{line}</yellow> | "
            "<cyan>{message}</cyan>"
        ),
        level="INFO",
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    return loguru_logger


logger = get_logger()
