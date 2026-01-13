#!/usr/bin/env python3
import argparse
import datetime
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

QUOTES = [
    "The sky is falling, but the coffee is still hot.",
    "When the world ends, remember to turn off the lights.",
    "Apocalypse is just a word; survival is a choice.",
    "The last sunset will be the brightest.",
    "In the end, we all become dust and data.",
    "The apocalypse is a good excuse for a nap.",
    "When the clocks stop, the jokes start.",
    "The end is just the beginning of a new playlist.",
    "If the world ends, at least the Wi-Fi will still work.",
    "Apocalypse: the ultimate test of patience.\"
]

def get_quote_for_date(date: datetime.date) -> str:
    index = date.toordinal() % len(QUOTES)
    return QUOTES[index]

def serve_http(port=8080):
    class QuoteHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/quote":
                date = datetime.date.today()
                quote = get_quote_for_date(date)
                payload = {"date": date.isoformat(), "quote": quote}
                response = json.dumps(payload).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response)))
                self.end_headers()
                self.wfile.write(response)
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, format, *args):
            return  # suppress logging

    server = HTTPServer(('', port), QuoteHandler)
    print(f"Serving on port {port}")
    server.serve_forever()

def main():
    parser = argparse.ArgumentParser(description="Daily apocalypse quote")
    parser.add_argument("--quote", action="store_true", help="Print today's quote")
    parser.add_argument("--serve", action="store_true", help="Run HTTP server")
    args = parser.parse_args()

    if args.quote:
        date = datetime.date.today()
        print(get_quote_for_date(date))
    elif args.serve:
        serve_http()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

