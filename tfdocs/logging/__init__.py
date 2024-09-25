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
from tfdocs.logging.setup import setup_logs

traceback.install()

def cleanup_log_file(log_file) -> Result[None, OSError]:
    if os.path.exists(log_file.name):
        log_file.close()
        result = try_wrap(os.remove, log_file.name)
    return Ok(None)

__all__ = ['setup_logs']
