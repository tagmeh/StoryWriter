from os import system

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Label


class MainPageApp(App[str]):
    TITLE = "Main Page"
    SUB_TITLE = "Landing page for StoryWriter"

    def on_mount(self) -> None:
        """Updates the TUI settings on load."""
        self.screen.styles.background = "black"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Yo yo yo")
        yield Button("Yes", id="yes", variant="primary")
        yield Button("No", id="no", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)


class SuspendingApp(App[None]):

    def compose(self) -> ComposeResult:
        yield Button("Open the editor", id="edit")

    @on(Button.Pressed, "#edit")
    def run_external_editor(self) -> None:
        with self.suspend():
            # If system is windows
            system("bash -c 'nano \"stories/{story_name}/inputs/system_prompt.txt\"'")
            # If system is linux
            system("nano 'stories/{story_name}/inputs/system_prompt.txt'")


if __name__ == "__main__":
    app = SuspendingApp()
    app.run()
