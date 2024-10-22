"""
    This component is used for a few things, and is the most multi-purpose widget.
    It is in charge of things like switching between providers, viewing the user's
    history, and more.
"""

import logging

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, TabbedContent, TabPane
from textual.binding import Binding
from textual import log
from typing import Callable


class Special(Vertical, can_focus=True):
    DEFAULT_CSS = """
        Special {
            height: 100%;
            background: $panel;
            border: round $primary;
        }

        Special > Static {
            width: auto;
            height: 10%;
            margin-right: 1;
            background: $boost;
        }

        Special:focus {
            border: round $accent;
        }
    """
    BINDINGS = [
        ("1", "open_tab_index(1)"),
        ("2", "open_tab_index(2)"),
        ("3", "open_tab_index(3)"),
        ("4", "open_tab_index(4)"),
        ("5", "open_tab_index(5)"),
    ]

    def __init__(self, id="special", classes="") -> None:
        self.tabs: list[tuple[str, Callable]] = [
            ("providers", lambda: Static("providers will go here")),
            ("history", lambda: Static("history will go here")),
            ("search", lambda: Static("search will go here")),
            ("sync", lambda: Static("sync will go here")),
            ("help", lambda: Static("help will go here")),
        ]
        super().__init__(id=id, classes=classes)

    def compose(self) -> ComposeResult:
        with TabbedContent():
            for i, tab in enumerate(self.tabs):
                with TabPane(f"[{i+1}]{tab[0]}", id=tab[0]):
                    yield tab[1]()

    def action_open_tab_index(self, i):
        new_tab = self.tabs[i - 1][0]
        log("Opening " + new_tab)
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.active = new_tab
