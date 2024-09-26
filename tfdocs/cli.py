import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Terraform Documentation in the Terminal")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase output verbosity (-v, -vv)"
    )
    parser.add_argument(
        "--serve-logs", action="store_true", default=False, help="Send logs to log viewing server"
    )

    args = vars(parser.parse_args())

    # make sure verbosity is in the correct range and prepare for logging module
    if args["verbose"] not in range(0,3):
        raise argparse.ArgumentError(None, "Incorrect number of 'verbose' flags applied")
    args["verbose"] = 30 - 10 * args["verbose"]

    return args
