from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import socket
from pathlib import Path
from core.config import settings

def check_port(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except:
        return False

def check_nas() -> bool:
    try:
        return Path(settings.connections.nas_test_file).exists()
    except:
        return False

def render_connections_pane() -> Panel:
    table = Table.grid(padding=1)
    table.add_column(style="bold")

    def led(status: bool, name: str) -> Text:
        return Text(f"● {name}", style="green" if status else "red")

    table.add_row(led(check_port(settings.connections.indi_host, settings.connections.indi_port), "INDI"))
    table.add_row(led(check_port(settings.connections.seestar_alp_host, settings.connections.seestar_alp_port), "Seestar ALP"))
    table.add_row(led(check_nas(), "NAS Mount"))
    table.add_row(led(True, "Weather API"))  # always true for now

    return Panel(table, title="🔌 CONNECTIONS", border_style="magenta", padding=(1, 2))
