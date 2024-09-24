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

def get_logger(name_override: str | None= None, log_level: int | None = None, stream=False) -> Logger:

    propagate = True
    if name_override is None:
        name_override = __name__.split('.')[0]
        propagate = False
        print(propagate)

    logger: Logger = logging.getLogger(name_override)
    logger.setLevel(logging.DEBUG)
    logger.propagate = propagate

    # if it's a brand new logger then add all the required handlers
    if not logger.hasHandlers():
        # setup tempfile logging
        file_handler = make_file_handler()
        # setup rich console logging
        console_handler = make_console_handler()
        
        if stream:
            http_handler = make_http_handler()
            http_handler.setLevel(logging.DEBUG)
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
                if log_level is not None:
                    handler.setLevel(log_level)
                else:
                    handler.setLevel(logging.WARNING)
    return logger

def make_file_handler() -> logging.FileHandler:
    # create tempfile
    os.makedirs("/tmp/tfdocs", exist_ok=True)
    temp_log_file = tempfile.NamedTemporaryFile(
        delete = False,
        suffix = ".log",
        mode = 'w',
        dir="/tmp/tfdocs"
    )

    # create file-handler
    handler = logging.FileHandler(temp_log_file.name)
    handler.setLevel(logging.DEBUG)

    format = "%(asctime)s %(levelname)s | %(message)s"
    formatter = logging.Formatter(format, datefmt="%H:%M:%S")
    handler.setFormatter(formatter)

    return handler

def make_console_handler():
    # create rich formatted console handler
    handler = RichHandler(log_time_format="[%X]")
    # default logging level is set to warning
    handler.setLevel(logging.WARNING)
    return handler

def make_http_handler():
    # used to stream logs to a local http server, handy for development.
    handler = HTTPHandler("localhost:1234","log")
    format = "%(asctime)s %(levelname)s | %(message)s"
    handler.setFormatter(format)
    return handler

def cleanup_log_file(log_file) -> Result[None, OSError]:
    if os.path.exists(log_file.name):
        log_file.close()
        result = try_wrap(os.remove, log_file.name)
    return Ok(None)
