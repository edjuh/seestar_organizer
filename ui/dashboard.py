"""
Dashboard.
"""

from rich.live import Live
from rich.layout import Layout
from time import sleep
from loguru import logger

from core.config import settings
from core.weather.monitor import safety_monitor
from ui.top_bar import render_top_bar
from ui.conditions_pane import render_conditions_pane
from ui.connections_pane import render_connections_pane
from ui.keyboard import show_help

def run_dashboard() -> None:
    layout = Layout()
    layout.split(
        Layout(name="top", size=3),
        Layout(name="body", ratio=1),
    )
    layout["body"].split_row(
        Layout(name="conditions", ratio=1),
        Layout(name="connections", ratio=1),
    )

    safety_monitor.start()
    logger.info("Dashboard + SafetyMonitor running")

    show_help()

    try:
        with Live(layout, refresh_per_second=4, screen=True) as live:
            while True:
                layout["top"].update(render_top_bar())
                layout["conditions"].update(render_conditions_pane())
                layout["connections"].update(render_connections_pane())
                live.update(layout)
                sleep(settings.general.dashboard_refresh_seconds)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    finally:
        safety_monitor.stop()
        logger.success("Seestar Organizer shutdown clean")
