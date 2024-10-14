from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Static, Footer, Button, ContentSwitcher
from tfdocs.views.viewer import Viewer
from tfdocs.views.switcher import Switcher
from tfdocs.views.special import Special


def main():
    app = ComponentViewer()
    app.run()


class ComponentViewer(App):
    CSS_PATH = "styles/component_viewer.tcss"
    # DEFAULT_CSS = """
    #     Screen {
    #         align: center middle;
    #         /* padding: 1; */
    #     }

    #     #buttons {
    #         height: 3;
    #         width: auto;
    #     }

    # """
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        with Horizontal(id="buttons"):
            yield Button("Viewer", id="viewer")
            yield Button("Switcher", id="switcher")
            yield Button("Special", id="special")
        with ContentSwitcher(id="component_viewer", initial="viewer"):
            yield Special(id="special")
            yield Viewer(id="viewer", classes="")
            yield Switcher(id="switcher", classes="pane")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id
