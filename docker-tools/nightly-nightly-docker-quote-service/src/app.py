#!/usr/bin/env python3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone

QUOTES = [
    "The ashes whisper, \"Tomorrow is a myth.\"",
    "Radiation roses bloom in the night.",
    "Silence is louder than the last siren.",
    "Dust knows all secrets of the fallen.",
    "Hope is a candle in a storm of static."
]

def get_quote(date: datetime = None) -> str:
    """Return a deterministic quote based on the UTC day of year.

    If *date* is None the current UTC datetime is used.
    """
    if date is None:
        date = datetime.now(timezone.utc)
    index = date.timetuple().tm_yday % len(QUOTES)
    return QUOTES[index]

class QuoteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/quote":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return
        quote = get_quote()
        payload = json.dumps({"quote": quote}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

def run(host="0.0.0.0", port=8080):
    server = HTTPServer((host, port), QuoteHandler)
    print(f"Starting quote server on http://{host}:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
