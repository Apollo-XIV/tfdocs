from tfdocs.logging import setup_logs
import logging

def main():
    setup_logs(
        print_log_level=30,
        enable_log_streaming=True
    )
    log = logging.getLogger(__name__)
    log.debug("test message")
    log.warning("test warning message")
    log.critical("Oh my, its a message!")
