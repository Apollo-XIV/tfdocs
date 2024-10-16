"""
    This component is used to format and organise the panes that make up the app.
    It is reponsible for ensuring that at whatever screen-size the UI is legible
    and the UX is pleasant.
"""

from textual import log
from textual.screen import Screen
from textual.app import ComposeResult 
from textual.widgets import Static
from textual.reactive import reactive
from textual.containers import Container
from textual.binding import Binding

from tfdocs.views.viewer import Viewer
from tfdocs.views.switcher import Switcher

class PaneLayout(Static):
    BINDINGS = [
        Binding("tab", "cycle_focus", priority=True),
        Binding("shift+tab", "cycle_focus_previous", priority=True),
    ]

    provider = reactive("test ", recompose=True)

    def compose(self) -> ComposeResult:
        yield Static("Test widget")
        with Container(id="app-grid"):
            yield Viewer(classes="pane")
            yield Switcher(classes="pane").data_bind(PaneLayout.provider)

    async def action_cycle_focus(self):
        log(self.children)
        self.query_one(Viewer).focus()


    async def action_cycle_focus_previous(self):
        self.query_one(Screen).focus_previous(selector=".pane")

