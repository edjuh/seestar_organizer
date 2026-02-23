import socket
import json
import time

def tap_wire():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect(("localhost", 2947))
        s.sendall(b'?WATCH={"enable":true,"json":true};\n')
        
        print("Connected. Tapping port 2947 for 10 seconds...\n")
        
        f = s.makefile('r')
        start_time = time.time()
        
        while time.time() - start_time < 10:
            line = f.readline()
            if not line:
                break
            
            try:
                msg = json.loads(line)
                print(f"[{msg.get('class', 'UNKNOWN')}] {line.strip()[:100]}...")
            except json.JSONDecodeError:
                print(f"[RAW ERROR] {line.strip()}")
                
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    tap_wire()
