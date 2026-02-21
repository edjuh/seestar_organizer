from datetime import datetime
from zoneinfo import ZoneInfo
from rich.console import Console
from rich.text import Text
from core.config import settings
from utils.astro import get_moon_illumination

console = Console()

def render_top_bar() -> Text:
    now_utc = datetime.now(ZoneInfo("UTC"))
    now_local = now_utc.astimezone(ZoneInfo(settings.location.timezone))

    moon = get_moon_illumination()

    bar = Text()
    bar.append(f" {settings.general.project_name} v{settings.general.version} ", style="bold cyan")
    bar.append(" | ")
    bar.append(f"UTC {now_utc.strftime('%H:%M:%S')} ", style="white")
    bar.append(f"Local {now_local.strftime('%H:%M:%S')} ", style="green")
    bar.append(" | ")
    bar.append(f"{settings.location.city} • {settings.location.maidenhead_locator} ", style="yellow")
    bar.append(" | ")
    bar.append(f"Moon: {moon['phase']} {moon['illumination_percent']}% ", style="magenta")

    return bar
