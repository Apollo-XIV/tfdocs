import argparse
import tfdocs.logging.watch_logs as watch_logs


def default_hello():
    print("Default Command")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Terraform Documentation in the Terminal"
    )

    # default command
    parser.set_defaults(func=default_hello)

    # subcommands
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    subcommands = {"watch-logs": watch_logs.parse_args}

    for key, command in subcommands.items():
        command(subparsers)

    # global options
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase output verbosity (-v, -vv)",
    )
    parser.add_argument(
        "--serve-logs",
        action="store_true",
        default=False,
        help="Send logs to log viewing server",
    )

    # try:
    args = vars(parser.parse_args())
    # except SystemExit as e:
    # print("test")
    # raise argparse.ArgumentError(None, e)

    command_key = args["command"]

    # if command_key not in subcommands and command_key is not None:
    #     raise argparse.ArgumentError(None, f"Invalid command '{command_key}'")

    # make sure verbosity is in the correct range and prepare for logging module
    if args["verbose"] not in range(0, 3):
        raise argparse.ArgumentError(
            None, "Incorrect number of 'verbose' flags applied"
        )
    args["verbose"] = 30 - 10 * args["verbose"]

    return parser, args
