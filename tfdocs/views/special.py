"""
    This component is used for a few things, and is the most multi-purpose widget.
    It is in charge of things like switching between providers, viewing the user's
    history, and more.
"""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, TabbedContent, TabPane
from textual.binding import Binding


class Special(Vertical):
    DEFAULT_CSS = """
        Special {
            height: 100%;
            background: $panel;
            border: hkey $primary;
        }

        Special > Static {
            width: auto;
            height: 10%;
            margin-right: 1;
            background: $boost;
        }

        Special:focus {
            border: hkey $accent;
        }
    """

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("\[1]providers", id="providers"):
                yield Static("Test")
            with TabPane("\[2]history", id="history"):
                yield Static("Test")
            with TabPane("\[3]search", id="search"):
                yield Static("Test")
            with TabPane("\[4]sync", id="sync"):
                yield Static("Test")
            with TabPane("\[5]help", id="help"):
                yield Static("Test")
