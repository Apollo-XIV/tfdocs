import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="A modular argparse command processor.")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase output verbosity (-v, -vv)"
    )

    args = vars(parser.parse_args())
    if args["verbose"] not in range(0,3):
        raise argparse.ArgumentError(None, "Incorrect number of 'verbose' flags applied")
    args["verbose"] = 30 - 10 * args["verbose"]

    return args
