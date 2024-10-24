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

class Switcher(Vertical, can_focus=True):
    DEFAULT_CSS = """
        Switcher {
            background: $panel;
            border: round $primary;
            width: 100%;
        }

        Switcher:focus {
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
        ("j", "cursor_down"),
        ("k", "cursor_up"),
        ("h", "cursor_left"),
        ("l", "cursor_right"),
        ("u", "page_up"),
        ("d", "page_down"),
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

    def action_cursor_down(self):
        active_pane = self.query_one(TabbedContent).active_pane
        active_pane.get_child_by_id("list").action_cursor_down()

    def action_cursor_up(self):
        active_pane = self.query_one(TabbedContent).active_pane
        active_pane.get_child_by_id("list").action_cursor_up()

    def action_cursor_left(self):
        tabbed_content = self.query_one(TabbedContent)
        n = self.tabs.index(tabbed_content.active)
        tabbed_content.active = self.tabs[n - 1 % tabbed_content.tab_count]

    def action_cursor_right(self):
        tabbed_content = self.query_one(TabbedContent)
        n = self.tabs.index(tabbed_content.active)
        tabbed_content.active = self.tabs[(n + 1) % tabbed_content.tab_count]

        # log(self.query_one("#"+active).get_child_by_id(f"{active}-list").action_cursor_down())

    # async def on_mount(self) -> None:
    #     self.focus()
    #     test_resources = [Option(f" test{i}", id=i) for i in range(15)]
    #     self.add_options(test_resources)
    # self.run_worker(load_resources(), exclusive=True)
    # self.mount(Search())

    def scroll_to_option(self, name):
        opt = self.get_option(name)
        self.highlighted = opt.index
        self.scroll_to_highlight(top=True)

    # '''
    #     Handles the result of the load_resources function and adds them as options
    # '''
    # @on(Worker.StateChanged)
    # async def handle_resources(self, event: Worker.StateChanged) -> None:
    #   if event.worker.name == "load_resources" and event.worker.is_finished and event.state == WorkerState.SUCCESS:
    #       opts = [ResourceOpt(r_id, index=i) for i, r_id in enumerate(event.worker.result)]
    #       self.add_options(opts)
