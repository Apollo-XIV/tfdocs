import tempfile
import os
import logging
import atexit
from logging import Logger
from rich import traceback
from result import as_result, Ok, Result
from tfdocs.utils import try_wrap

traceback.install()

def get_logger(name_override: str = __name__, log_level: int = logging.INFO) -> Logger:
    logger = logging.getLogger(name_override)
    logger.setLevel(log_level)

    if not logger.hasHandlers():
        # setup tempfile logging
        file_handler = file_handler()
        # setup rich console logging
        
        logger.addHandler(file_handler)
  
    return logger

def file_handler() -> logging.FileHandler:
    # create tempfile
    temp_log_file = tempfile.NamedTemporaryFile(
        delete = False,
        suffix = ".log",
        mode = 'w'
    )
    
    print(f"Logging to temporary file {temp_log_file.name}")
    handler = logging.FileHandler(temp_log_file.name)
    handler.setLevel(logging.DEBUG)

    atexit.register(cleanup_log_file, temp_log_file.name)
    return handler

def cleanup_log_file(log_file) -> Result[None, OSError]:
    if os.path.exists(log_file.name):
        log_file.close()
        result = try_wrap(os.remove, log_file.name)
        if result.is_ok():
            print("I'm okay!")
        elif result.is_err():
            print("I'm not okay!")
    return Ok(None)
