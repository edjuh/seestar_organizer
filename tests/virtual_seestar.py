from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class VirtualSeestarHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress the default messy HTTP logging
        pass

    def do_POST(self):
        if self.path == "/api/v1/telescope/0/sequence":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                payload = json.loads(post_data)
                print("\n[VIRTUAL SEESTAR] 🚨 INCOMING MISSION PAYLOAD 🚨")
                print(json.dumps(payload, indent=2))
                print("[VIRTUAL SEESTAR] ⚙️  Simulating 1x1 Mosaic Plate-Solve...")
                print("[VIRTUAL SEESTAR] ✅ Mission Accepted.\n")
                
                self.send_response(202) # 202 Accepted
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"ErrorNumber": 0, "ErrorMessage": "Mock sequencer accepted plan"}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def run_mock():
    port = 5555
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, VirtualSeestarHandler)
    print(f"🔭 Virtual Seestar online and listening on http://0.0.0.0:{port}")
    print("   Waiting for Alpaca Sequencer payloads... (Press CTRL+C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🔭 Virtual Seestar shutting down.")
        httpd.server_close()

if __name__ == "__main__":
    run_mock()
