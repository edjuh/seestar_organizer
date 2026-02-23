from flask import Flask, render_template
import json
import os

# Absolute paths using OS module
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(CURRENT_DIR, "templates")
STATE_FILE = os.path.join(os.path.dirname(CURRENT_DIR), "data", "system_state.json")

print(f"🔧 Booting AlarmPI...")
print(f"📂 Looking for templates in: {TEMPLATE_DIR}")
print(f"📄 Checking if index.html exists: {os.path.exists(os.path.join(TEMPLATE_DIR, 'index.html'))}")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

@app.route("/")
def index():
    state_data = {"status": "UNKNOWN", "target": "None", "message": "No data"}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                state_data = json.load(f)
        except Exception as e:
            print(f"⚠️ Error reading state: {e}")
            pass
            
    bg_color = "#2c3e50"
    if state_data["status"] == "WORKING":
        bg_color = "#27ae60"
    elif state_data["status"] == "DEFCON_1":
        bg_color = "#c0392b"
    elif state_data["status"] == "ERROR":
        bg_color = "#f39c12"
    elif state_data["status"] == "COMPLETE":
        bg_color = "#2980b9"

    return render_template("index.html", state=state_data, bg_color=bg_color)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
