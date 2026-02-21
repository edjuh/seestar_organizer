import time
import tomllib
from flask import Flask
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import threading

# Core Logic Imports
from core.weather import WeatherGate
from core.organizer import Organizer
from core.seestar_client import SeestarClient

# 1. Load Configuration
with open("config.toml", "rb") as f:
    CONFIG = tomllib.load(f)

# 2. Initialize Components
weather = WeatherGate(
    lat=CONFIG['location']['lat'], 
    lon=CONFIG['location']['lon'], 
    api_key=CONFIG['weather']['meteoblue_apikey']
)
organizer = Organizer(CONFIG)
# Seestar client points to our Alpaca bridge on 5555
client = SeestarClient(host=CONFIG['alpaca']['host'], port=CONFIG['alpaca']['port'])

# 3. Global State for Dashboard
state = {
    "weather_status": "Initializing...",
    "weather_safe": False,
    "alpaca_status": "Disconnected",
    "last_update": "N/A",
    "engine_mode": "IDLE"
}

# 4. The "Autonomy Engine" Loop
def engine_loop():
    print("[ENGINE] Starting Autonomy Loop...")
    while True:
        try:
            # UNPACKING THE TUPLE: (is_safe, message)
            is_safe, msg = weather.check_safety(simulate=True)
            
            state["weather_safe"] = is_safe
            state["weather_status"] = msg
            
            # Check Alpaca Connection
            if client.is_connected():
                state["alpaca_status"] = "CONNECTED"
            else:
                state["alpaca_status"] = "OFFLINE (Check Bridge)"

            state["last_update"] = time.strftime("%H:%M:%S")
            
            # Logic Gate
            if not is_safe:
                state["engine_mode"] = "PARKED (Unsafe Weather)"
            else:
                state["engine_mode"] = "ACTIVE (Monitoring)"

            time.sleep(10) # 10-second heartbeat
        except Exception as e:
            print(f"[ENGINE ERROR] {e}. Retrying...")
            time.sleep(5)

# Start Engine in Background
threading.Thread(target=engine_loop, daemon=True).start()

# 5. Dashboard UI (Dash)
app = Dash(__name__)
server = app.server

app.layout = html.Div(style={'backgroundColor': '#1a1a1a', 'color': '#ffffff', 'padding': '20px', 'fontFamily': 'sans-serif'}, children=[
    html.H1("S30-PRO Autonomy Pilot", style={'textAlign': 'center', 'color': '#00ff00'}),
    html.Hr(),
    html.Div([
        html.H3(f"System Mode: {state['engine_mode']}"),
        html.P(f"Last Heartbeat: {state['last_update']}"),
    ], style={'padding': '10px', 'border': '1px solid #333'}),
    
    html.Div([
        html.Div([
            html.H4("Weather Gate"),
            html.P(id='weather-text', children=state['weather_status']),
            html.Div(style={'height': '20px', 'width': '100%', 'backgroundColor': 'green' if state['weather_safe'] else 'red'})
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.H4("Alpaca Bridge"),
            html.P(id='alpaca-text', children=state['alpaca_status']),
            html.Div(style={'height': '20px', 'width': '100%', 'backgroundColor': 'green' if state['alpaca_status'] == "CONNECTED" else 'orange'})
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '10px'}),
    ]),
    
    dcc.Interval(id='interval-component', interval=2*1000, n_intervals=0)
])

@app.callback(
    [Output('weather-text', 'children'), Output('alpaca-text', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_metrics(n):
    return state['weather_status'], state['alpaca_status']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=False)
