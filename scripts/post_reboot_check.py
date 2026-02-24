import socket
import sys

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

ports = {5432: "Web UI", 5555: "Alpaca API", 7556: "Image API"}
print("--- Post-Reboot Specialist Status ---")
for port, name in ports.items():
    status = "✅ ONLINE" if check_port(port) else "❌ OFFLINE"
    print(f"Port {port} ({name}): {status}")

if not check_port(5555):
    print("\n⚠️ Specialist Alert: Bridge not detected. Run 'python3 root_app.py' in seestar_alp.")
