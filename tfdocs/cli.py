import logging
import argparse
from textual import on
from textual.app import App
from textual.widgets import OptionList
from rapidfuzz import fuzz
import tfdocs.logging.watch_logs as watch_logs
import tfdocs.db.args as init
from tfdocs.models.blocks.provider import Provider
from tfdocs.views.app import app


def parse_args():
    parser = argparse.ArgumentParser(
        description="Terraform Documentation in the Terminal"
    )

    # default command
    parser.set_defaults(func=app)

    # subcommands
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    subcommands = {
        "init": init.parse_args,
        "watch-logs": watch_logs.parse_args,
    }

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
    parser.add_argument(
        "-p",
        "--provider",
        action="store",
        default=None,
        help="Send logs to log viewing server",
    )

    args = vars(parser.parse_args())

    # make sure verbosity is in the correct range and prepare for logging module
    if args["verbose"] not in range(0, 3):
        raise argparse.ArgumentError(
            None, "Incorrect number of 'verbose' flags applied"
        )
    args["verbose"] = 30 - 10 * args["verbose"]

    return parser, args


def select_provider(query: str) -> Provider:
    """
        Process the given user input and figure out exactly what provider they 
        want to open
    """
    MATCH_THRESHHOLD = 60
    # fuzzy search for a provider by name in the database
    providers = [
        p for p in Provider.list_providers()
        if fuzz.partial_ratio(query, p.name) > MATCH_THRESHHOLD
    ]
    # if more than one is found, prompt the user to select one
    if len(providers) > 1:
        selector = SelectProvider([p.name for p in providers])
        i = selector.run(inline=True)
        print(i)
        return providers[i]
    # if exactly one is found, return that
    if len(providers) == 1:
        return providers[0]
    # if none are found error and exit
    else:
        raise ValueError("Couldn't find a provider matching that query")


class SelectProvider(App):
    def __init__(self, options: list[str]):
        self.options = options
        super().__init__()

    def compose(self):
        yield OptionList(*self.options)

    @on(OptionList.OptionSelected)
    def on_option_list_option_selected(self, event):
        print("AAAAAAAAAAa")
        print(event)
        self.exit(0)
