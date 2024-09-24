from logging import Logger
import tempfile
from tfdocs.logging import get_logger, cleanup_log_file

log = get_logger()
log = get_logger(__name__, log_level=20, stream=True)

def test_get_logger():
    logger1 = get_logger(__name__)
    logger2 = get_logger(__name__)
    assert isinstance(logger1, Logger)
    assert logger1 is logger2

def test_log_file_cleanup(monkeypatch):
    temp_log_file = tempfile.NamedTemporaryFile(
        delete = False,
        suffix = ".log",
        mode = 'w'
    )
    cleanup_log_file(temp_log_file)

def test_differing_verbosity():
    for i in range(30, 0, -10):
        log = get_logger(__name__, log_level=i)
        print(f"{i} ------------------------")
        log.warning("I should always be visible")
        log.info("I should only show when verbosity is <=20")
        log.debug("I should only show when verbosity is <=10")

