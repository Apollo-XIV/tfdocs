from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Static, Footer, Button, ContentSwitcher
from tfdocs.views.viewer import Viewer
from tfdocs.views.switcher import Switcher

def main():
    app = ComponentViewer()
    app.run()

class ComponentViewer(App):
    CSS_PATH="styles/component_viewer.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        with Horizontal(id="buttons"):
            yield Button("Blank", id="blank")
            yield Button("Viewer", id="viewer")
            yield Button("Switcher", id="switcher")
        with ContentSwitcher(initial="blank"):
            yield Static(id="blank")
            yield Viewer(id="viewer", classes="")
            yield Switcher(id="switcher", classes="pane")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id

