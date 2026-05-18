from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from datetime import datetime

console = Console()


def timestamp():
    return datetime.now().strftime("%H:%M:%S")


def log_info(message):
    console.print(
        f"[cyan][{timestamp()}][/cyan] {message}"
    )


def log_success(message):
    console.print(
        f"[green][{timestamp()}][/green] {message}"
    )


def log_error(message):
    console.print(
        f"[red][{timestamp()}][/red] {message}"
    )


def giant_alert(message):
    text = Text(
        f"\n{message}\n",
        justify="center",
        style="bold white on red"
    )

    console.print(
        Panel.fit(
            text,
            border_style="bright_yellow"
        )
    )