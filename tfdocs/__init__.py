from tfdocs.logging import setup_logs
from tfdocs.cli import parse_args
import logging

def main():
    parser, args = parse_args()

    setup_logs(
        print_log_level=args["verbose"],
        enable_log_streaming=args["serve_logs"]
    )
    log = logging.getLogger(__name__)

    if 'func' in args:
        log.info(f"Running command {args["command"]}")
        args["func"]()
    else: 
        parser.print_help()
        exit(0)
