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
        Binding("tab", "cycle_focus_forward", priority=True),
        Binding("shift+tab", "cycle_focus_back", priority=True),
    ]

    provider = reactive("test ", recompose=True)

    def compose(self) -> ComposeResult:
        yield Static("Test widget")
        with Container(id="app-grid"):
            yield Viewer(classes="pane")
            yield Switcher(classes="pane").data_bind(PaneLayout.provider)

    async def action_cycle_focus_forward(self):
        self.cycle_focus(forward=True)

    async def action_cycle_focus_back(self):
        self.cycle_focus(forward=False)

    def cycle_focus(self, forward=True):
        '''
            Cycles the focus of the application, or resets it onto the first pane
        '''
        res = self.query(".pane")
        # get all panes in the layout
        try:
            focussed_index = next(
                (i for i, child in enumerate(res) if child.has_focus == True)
            )
            # move to next pane
            focussed_index += 1 if forward else -1
            # loop round the panes
            focussed_index %= len(res)
        except StopIteration:
            # none of the panes are focussed, focus the first one
            focussed_index = 0

        res[focussed_index].focus()

        log(f"focussed: {res[focussed_index]}")
