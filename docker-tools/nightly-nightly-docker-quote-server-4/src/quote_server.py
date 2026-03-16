#!/usr/bin/env python3
import http.server
import socketserver
import random

QUOTES = [
    "The sun rose, but the world stayed dark.",
    "Even the shadows have a deadline.",
    "Hope is a candle in a storm of ash.",
    "When the wind whispers, listen for the last song.",
    "Survival is a game of dice and dust."
]

class QuoteHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        quote = random.choice(QUOTES)
        self.wfile.write(quote.encode("utf-8"))

if __name__ == "__main__":
    with socketserver.TCPServer(("", 8080), QuoteHandler) as httpd:
        print("Serving on port 8080")
        httpd.serve_forever()
