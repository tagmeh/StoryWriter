from textual.app import App, ComposeResult
from textual.widgets import Button, Placeholder, Static


class Header(Placeholder):
    DEFAULT_CSS = """
        Header {
            height: 3;
            dock: top;
        }
        """


class Footer(Placeholder):
    DEFAULT_CSS = """
        Footer {
            height: 3;
            dock: bottom;
        }
        """


class MainPageApp(App[str]):
    TITLE = "Main Page"
    SUB_TITLE = "Landing page for StoryWriter"
    CSS_PATH = "../css/main_page.tcss"

    def on_mount(self) -> None:
        """Updates the TUI settings on load."""

        self.screen.styles.background = "black"

    def compose(self) -> ComposeResult:
        yield Header(id="Header")
        yield Static("StoryWriter", id="title")
        yield Static(
            "Create or Modify an outline using a large language model, local or remote",
            id="subtitle",
        )
        yield Button("Create New Story", id="create", variant="success")
        yield Button("Edit Existing Story", id="edit", variant="primary")
        yield Button("Settings", id="settings", variant="default")
        yield Button("Exit", id="exit", variant="error")
        yield Footer(id="Footer")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit":
            self.exit()

        if event.button.id == "create":
            print("create")


if __name__ == "__main__":
    app = MainPageApp()
    app.run()
