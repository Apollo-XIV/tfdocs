import tempfile
import os
import logging
import atexit
from logging import Logger
from logging.handlers import HTTPHandler
from rich import traceback
from rich.logging import RichHandler
from result import as_result, Ok, Result
from tfdocs.utils import try_wrap

traceback.install()

def get_logger(name_override: str | None= None, log_level: int = logging.WARNING, stream=False) -> Logger:
    propagate = True
    if name_override is None:
        name_override = __name__.split('.')[0]
        propagate = False
    logger: Logger = logging.getLogger(name_override)
    logger.setLevel(log_level)
    logger.propagate = False

    # if it's a brand new logger then add all the required handlers
    if not logger.hasHandlers():
        # setup tempfile logging
        file_handler = make_file_handler()
        # setup rich console logging
        console_handler = make_console_handler()
        
        if stream:
            http_handler = make_http_handler()
            logger.addHandler(http_handler)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        for handler in logger.handlers:
            if isinstance(handler, logging.FileHandler):
                output_file = handler.baseFilename
        logger.info(f"Logging to {output_file}")
    # otherwise, update it with local settings
    else:
        for handler in logger.handlers:
            if isinstance(handler, RichHandler):
                handler.setLevel(log_level)
    return logger

def make_file_handler() -> logging.FileHandler:
    # create tempfile
    temp_log_file = tempfile.NamedTemporaryFile(
        delete = False,
        suffix = ".log",
        mode = 'w'
    )

    handler = logging.FileHandler(temp_log_file.name)
    handler.setLevel(logging.DEBUG)

    format = "%(asctime)s %(levelname)s | %(message)s"
    formatter = logging.Formatter(format, datefmt="%H:%M:%S")
    handler.setFormatter(formatter)

    return handler

def make_console_handler():
    handler = RichHandler(log_time_format="[%X]")
    return handler

def make_http_handler():
    handler = HTTPHandler("localhost:1234","log")
    format = "%(asctime)s %(levelname)s | %(message)s"
    handler.setFormatter(format)
    handler.setLevel(logging.DEBUG)
    return handler

def cleanup_log_file(log_file) -> Result[None, OSError]:
    if os.path.exists(log_file.name):
        log_file.close()
        result = try_wrap(os.remove, log_file.name)
    return Ok(None)
