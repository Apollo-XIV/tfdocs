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
    log.info(f"Running-subcommand {args["command"]}")

    if 'func' in args:
        args["func"]()
    else: 
        parser.print_help()
