from textual.app import App, ComposeResult
from textual.widgets import Footer

from tfdocs.views.layout import PaneLayout


class TFDocs(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield PaneLayout()
        yield Footer()


def app():
    app = TFDocs()
    app.run()
