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


def main():
    app = TFDocs()
    app.run()


if __name__ == "__main__":
    main()
