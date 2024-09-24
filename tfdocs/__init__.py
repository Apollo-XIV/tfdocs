from tfdocs.logging import get_logger
from tfdocs.logging.setup import setup_logs
import logging

def main():
    setup_logs()
    log = logging.getLogger()
    # log = get_logger(__name__, stream=True)
    log.debug("test message")
    log.warning("test message")
    log.critical("Oh my, its a message!")
