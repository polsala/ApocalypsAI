import unittest
from unittest.mock import patch
import datetime
import subprocess
import json
import requests
import os
import sys
import time

class TestApocalypseQuote(unittest.TestCase):
    def test_cli_quote(self):
        # Patch date to 2025-12-09
        with patch('datetime.date') as mock_date:
            mock_date.today.return_value = datetime.date(2025, 12, 9)
            mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
            result = subprocess.run([sys.executable, "src/main.py", "--quote"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            # Determine expected quote
            quotes = [
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
            index = datetime.date(2025,12,9).toordinal() % len(quotes)
            expected = quotes[index]
            self.assertEqual(result.stdout.strip(), expected)

    def test_http_server(self):
        # Start server in a separate process
        proc = subprocess.Popen([sys.executable, "src/main.py", "--serve"])
        time.sleep(1)  # give it time to start
        try:
            resp = requests.get("http://localhost:8080/quote")
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertIn("date", data)
            self.assertIn("quote", data)
            # Verify quote matches expected for today's date
            today = datetime.date.today()
            quotes = [
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
            index = today.toordinal() % len(quotes)
            expected = quotes[index]
            self.assertEqual(data["quote"], expected)
            self.assertEqual(data["date"], today.isoformat())
        finally:
            proc.terminate()
            proc.wait()

if __name__ == "__main__":
    unittest.main()

