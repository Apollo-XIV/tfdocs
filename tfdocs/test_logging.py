from logging import Logger
import tempfile
from tfdocs.logging import get_logger,cleanup_log_file

def test_get_logger():
    logger1 = get_logger()
    logger2 = get_logger()
    assert isinstance(logger1, Logger)
    assert logger1 is logger2

def test_log_file_cleanup(monkeypatch):
    temp_log_file = tempfile.NamedTemporaryFile(
        delete = False,
        suffix = ".log",
        mode = 'w'
    )
    cleanup_log_file(temp_log_file)

