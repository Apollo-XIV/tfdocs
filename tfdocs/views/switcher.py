from textual.app import ComposeResult
from textual import log
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import (
    Static,
    OptionList,
    TabbedContent,
    TabPane,
    MarkdownViewer,
    ContentSwitcher,
)
from textual.binding import Binding
from textual.widgets.option_list import Option

from tfdocs.views.list import List
from tfdocs.views.vertical import Vertical

class Switcher(Vertical, can_focus=True):
    DEFAULT_CSS = """
        Switcher {
            background: $panel;
            border: round $primary;
            width: 100%;
        }

        Switcher:focus-within {
            border: round $accent;
        }

		TabPane {
		    margin: 0;
		    padding: 0 0 !important;
		}

		TabbedContent > ContentSwitcher {
		    width: 100%;
		    height: 1fr;
            scrollbar-size: 1 1;
		}
    """
    BINDINGS = [
        ("h", "cursor_left"),
        ("l", "cursor_right"),
    ]

    provider: reactive[None] = reactive(None)

    def __init__(self, id: str = "switcher", classes: str = ""):
        self.tabs = ["resources", "data", "functions"]
        super().__init__(id=id, classes=classes)

    def compose(self) -> ComposeResult:
        test_resources = [Option(f"test-resource-{i}", id=str(i)) for i in range(15)]
        test_functions = [Option(f"test-functions-{i}", id=str(i)) for i in range(45)]
        test_data = [Option(f"test-data-{i}", id=str(i)) for i in range(90)]
        with TabbedContent():
            with TabPane("resources", id="resources"):
                yield List(test_resources, id="list")
            with TabPane("data", id="data"):
                yield List(test_data, id="list")
            with TabPane("functions", id="functions"):
                yield List(test_functions, id="list")

    def action_cursor_left(self):
        tabbed_content = self.query_one(TabbedContent)
        n = self.tabs.index(tabbed_content.active)
        tabbed_content.active = self.tabs[n - 1 % tabbed_content.tab_count]
        tabbed_content.active_pane.get_child_by_id("list").focus()

    def action_cursor_right(self):
        tabbed_content = self.query_one(TabbedContent)
        n = self.tabs.index(tabbed_content.active)
        tabbed_content.active = self.tabs[(n + 1) % tabbed_content.tab_count]
        tabbed_content.active_pane.get_child_by_id("list").focus()

    def scroll_to_option(self, name):
        opt = self.get_option(name)
        self.highlighted = opt.index
        self.scroll_to_highlight(top=True)

    def on_focus(self):
        active_pane = self.query_one(TabbedContent).active_pane
        active_pane.get_child_by_id("list").focus()
