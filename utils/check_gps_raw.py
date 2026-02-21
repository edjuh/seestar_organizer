import socket
import json

def check_gps():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 2947))
        s.sendall(b'?WATCH={"enable":true,"json":true};')
        
        print("Waiting for GPS sentence...")
        for _ in range(10):
            data = s.recv(4096).decode("utf-8")
            for line in data.split("\n"):
                if not line: continue
                msg = json.loads(line)
                if msg.get("class") == "TPV":
                    print(f"✅ GPS DATA FOUND: Lat: {msg.get('lat')}, Lon: {msg.get('lon')}, Mode: {msg.get('mode')}")
                    return
        print("❌ GPS connected but no TPV (Position) sentence received.")
    except Exception as e:
        print(f"❌ GPS Connection Failed: {e}")

if __name__ == "__main__":
    check_gps()
