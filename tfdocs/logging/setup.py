import logging
import logging.config
import os
import rich
import time
import tempfile
from rich.logging import RichHandler


def setup_logs(
    print_log_level: int = logging.WARNING,
    enable_log_streaming: bool = False
):
    format_str = "%(asctime)s %(levelname)s | %(message)s"
    date_format_str = "[%X]"
    log_file = make_log_file()
    
    logging.config.dictConfig({
        "version": 1,
        "format": format_str,
        "datefmt" : date_format_str,
        "propagate" : True,
        "loggers" : {
            "root" : {
                "handlers" : [
                    "console",
                    "file"
                ],
                "level" : 0,
            }
        },
        "handlers" : {
            "console" : {
                "class" : rich.logging.RichHandler,
                "filters" : ["verbosity"]
            },
            "file" : {
                "class" : logging.FileHandler,
                "filename" : log_file,     
                "formatter" : "precise",
            }
        },
        "formatters" : {
            "precise" : {
                "format" : format_str,
                "datefmt" : "[%x %X]"
            }
        },
        "filters" : {
            "verbosity": {
                "()": VerbosityFilter,
                "level": print_log_level
            }
        }
    })

    log = logging.getLogger()
    log.info(f"Logging to {log_file}")

def make_log_file() -> str:
    log_dir = "/tmp/tfdocs"
    # create logging directory
    os.makedirs(log_dir, exist_ok=True)

    # purge any logs older than 24 hours (make it a variable)
    now = time.time()
    retention_period = 24 * 60 * 60 # 24 hours in seconds

    for log_file in os.listdir(log_dir):
        log_file_path = os.path.join(log_dir, log_file)
        if os.path.isfile(log_file_path):
            file_mod_time = os.path.getmtime(log_file_path)
            if now - file_mod_time > retention_period:
                os.remove(log_file_path)

    # create new output file
    temp_log_file = tempfile.NamedTemporaryFile(
        delete = False,
        suffix = ".log",
        mode = 'w',
        dir="/tmp/tfdocs"
    )

    return temp_log_file.name
   
class VerbosityFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno >= self.level
