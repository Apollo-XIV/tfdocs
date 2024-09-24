import logging
import logging.config
import os
import tempfile
from rich.logging import RichHandler

def setup_logs(
        print_log_level: int = logging.WARNING
    ):
    format_str = "%(asctime)s %(levelname)s | %(message)s"
    date_format_str = "[%X]"
    logging.config.dictConfig({
        "version": 1,
        "format": format_str,
        "datefmt" : date_format_str,
        "level" : print_log_level,
        "handlers" : {
            "console" : {
                "class": "rich.logging.RichHandler",
            }
        }
    })

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
    
