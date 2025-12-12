import os
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

def get_current_time():
    override = os.getenv("TIME_OVERRIDE")
    if override:
        try:
            # Expect ISO format, allow trailing Z
            dt = datetime.fromisoformat(override.replace("Z", "+00:00"))
        except ValueError:
            dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    else:
        dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")

def get_message():
    # Whimsical static message
    return "The stars align in perfect harmony."

def build_response():
    return {
        "time": get_current_time(),
        "message": get_message()
    }

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_response(404)
            self.end_headers()
            return
        response = build_response()
        payload = json.dumps(response).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
