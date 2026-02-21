"""
Conditions pane now driven by background SafetyMonitor.
Big 4-color LED + live reasons.
"""

from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from core.weather.monitor import safety_monitor

def render_conditions_pane() -> Panel:
    state = safety_monitor.get_state()

    table = Table.grid(padding=(0, 1))
    table.add_column(justify="left")

    # Big safety LED
    led = Text(f"● {state['status']}", style=f"bold {state['color']} reverse")
    table.add_row(led)

    # Reasons or all-clear
    if state["reasons"]:
        for reason in state["reasons"]:
            table.add_row(Text(f"  ⚠ {reason}", style="yellow"))
    else:
        table.add_row(Text("  All conditions nominal ✓", style="green"))

    return Panel(
        table,
        title="🛡️ CONDITIONS",
        border_style=state["color"],
        padding=(1, 2)
    )
