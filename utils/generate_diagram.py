"""
Filename: utils/generate_diagram.py
Purpose: Generates a PNG flow diagram of the S30-PRO Autonomy Architecture.
"""
import graphviz

dot = graphviz.Digraph('S30_PRO_Architecture', filename='architecture_flow', format='png')
dot.attr(rankdir='LR', fontname='Helvetica', fontsize='12')

# --- Subsystems (The Sensors & Actuators) ---
with dot.subgraph(name='cluster_subsystems') as c:
    c.attr(label='Subsystems (Hardware/APIs)', style='rounded,filled', color='#e0e0e0')
    c.node('GPS', '📍 GPSMonitor\n(Serial/NMEA)', shape='box')
    c.node('WX', '⛈️ WeatherStation\n(Meteoblue/Safe)', shape='box')
    c.node('Brain', '🧠 TargetManager\n(AstroPy/Math)', shape='box')
    c.node('Hardware', '🔭 SeestarClient\n(Alpaca/Slew/Expose)', shape='box')
    c.node('Janitor', '🧹 FitsOrganizer\n(Disk IO/OpenCV)', shape='box')

# --- The Engine (The Brain) ---
with dot.subgraph(name='cluster_engine') as c:
    c.attr(label='AutonomyEngine (Daemon Thread)', style='rounded,filled', color='#d0e8f2')
    c.node('Loop', '⚙️ Main Execution Loop\n(Safety ➔ Target ➔ Slew ➔ Expose)', shape='ellipse', style='filled', fillcolor='white')
    c.node('State', '🔒 State Snapshot\n(Thread-Safe Dictionary)', shape='cylinder', style='filled', fillcolor='#fcfcba')
    
    c.edge('Loop', 'State', label=' Writes (Locked)')

# --- The UI (The Observer) ---
with dot.subgraph(name='cluster_ui') as c:
    c.attr(label='Presentation Layer', style='rounded,filled', color='#e8f2d0')
    c.node('UI', '🖥️ Dash Web Server\n(Read-Only UI)', shape='note')

# --- Connections ---
dot.edge('GPS', 'Loop', label=' Polled')
dot.edge('WX', 'Loop', label=' Polled')
dot.edge('Brain', 'Loop', label=' Computed')
dot.edge('Loop', 'Hardware', label=' Commanded')
dot.edge('Loop', 'Janitor', label=' Triggered')

dot.edge('State', 'UI', label=' 1Hz Decoupled Read\n(No Race Conditions)', style='dashed', color='blue')

dot.render(cleanup=True)
print("Diagram generated: architecture_flow.png")
