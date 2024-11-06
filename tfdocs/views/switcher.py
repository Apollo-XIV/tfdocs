import logging
from textual.app import ComposeResult, App
from textual import log, work
from textual.containers import Vertical
from textual.reactive import reactive
from textual.message import Message
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

from tfdocs.models.blocks.provider import Provider
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

    provider: reactive[Provider] = reactive(
        Provider.from_name("registry.terraform.io/hashicorp/archive")
    )

    def __init__(self, id: str = "switcher", classes: str = ""):
        self.tabs = ["resources", "data", "functions"]
        super().__init__(id=id, classes=classes)

    def on_mount(self):
        pass
        # self.run_worker(self.load_resources(self.provider), thread=True)
        # self.run_worker(self.load_datasources(self.provider), thread=True)

    def watch_provider(self, old, new):
        self.load_resources(new)
        # self.run_worker(self.load_datasources(new), thread=True)

    def compose(self) -> ComposeResult:
        # dispatch worker to load different values
        # resources = [Option(r[1], id=r[0]) for r in self.provider.list_resources()]
        functions = [
            Option(f"Function Documentation isn't available yet", id="not-implemented")
        ]
        # datasources = [
        #     Option(d[1], id=d[0]) for d in self.provider.list_datasources()
        # ]
        with TabbedContent():
            with TabPane("resources", id="resources"):
                yield List([], id="resource-list")
            with TabPane("data", id="data"):
                yield List([], id="datasource-list")
            with TabPane("functions", id="functions"):
                yield List(functions, id="list")

    def action_cursor_left(self):
        tabbed_content = self.query_one(TabbedContent)
        n = self.tabs.index(tabbed_content.active)
        tabbed_content.active = self.tabs[n - 1 % tabbed_content.tab_count]
        tabbed_content.active_pane.query_children(".list")[0].focus()

    def action_cursor_right(self):
        tabbed_content = self.query_one(TabbedContent)
        n = self.tabs.index(tabbed_content.active)
        tabbed_content.active = self.tabs[(n + 1) % tabbed_content.tab_count]
        tabbed_content.active_pane.query_children(".list")[0].focus()

    def scroll_to_option(self, name):
        opt = self.get_option(name)
        self.highlighted = opt.index
        self.scroll_to_highlight(top=True)

    def on_focus(self):
        active_pane = self.query_one(TabbedContent).active_pane
        active_pane.query_children(".list")[0].focus()

    @work(exclusive=True, thread=True)
    async def load_resources(self, provider: Provider):
        # clear current resources
        # rlist = self.query_one("#resource-list", expect_type=List)
        # self.call_from_thread(rlist.clear_options)
        # load new resources
        resources = [Option(r[1], id=r[0]) for r in self.provider.list_resources()]
        log(f"got the following resources from db: {resources}")
        # add in bulk
        self.post_message(self.LoadedEntities("Resource", resources))
        # App.call_from_thread(rlist.add_options, resources)

    async def load_datasources(self, provider: Provider):
        dlist = self.query_one("#datasource-list", expect_type=List)
        self.call_from_thread(dlist.clear_options)
        # load new datasources
        datasources = [Option(r[1], id=r[0]) for r in self.provider.list_datasources()]
        # add in bulk
        # App.call_from_thread(dlist.add_options, datasources)

    def on_switcher_loaded_entities(self, msg):
        olist = None
        block_type = msg.block_type
        log(f"Loaded Option Type: {block_type}")
        if block_type == "Resource":
            olist = self.query_one("#resource-list", expect_type=List)
        elif block_type == "DataSource":
            olist = self.query_one("#datasource-list", expect_type=List)
        else:
            raise ValueError("Tried to load an unexpected type of option")
        olist.clear_options()
        olist.add_options(msg.blocks)
        log("I RAN")

    class LoadedEntities(Message):
        def __init__(self, block_type: str, blocks: list[Option]):
            self.block_type = block_type
            self.blocks = blocks
            super().__init__()
