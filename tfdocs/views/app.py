from textual.app import App, ComposeResult
from textual.widgets import Footer

class TFDocs(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Footer()

def main():
    app = TFDocs()
    app.run()

if __name__ == "__main__":
    main()
