from tfdocs.logging import setup_logs
from tfdocs.cli import parse_args
import logging

def main():
    args = parse_args()
    setup_logs(
        print_log_level=args["verbose"],
        enable_log_streaming=True
    )
    log = logging.getLogger(__name__)
    log.debug("test message")
    log.warning("test warning message")
    log.critical("Oh my, its a message!")
