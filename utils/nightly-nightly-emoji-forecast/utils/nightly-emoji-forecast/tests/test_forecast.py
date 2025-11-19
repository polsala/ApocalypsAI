import unittest
from unittest.mock import patch
from src.forecast import get_emoji_forecast

class TestEmojiForecast(unittest.TestCase):
    @patch('hashlib.sha256')
    def test_deterministic_forecast(self, mock_sha):
        # Mock the hash to return a digest that maps to index 2 (rainy)
        class MockHash:
            def hexdigest(self):
                # Hex string that converts to an int where mod 5 == 2
                return '2' * 64
        mock_sha.return_value = MockHash()
        self.assertEqual(get_emoji_forecast("any-date"), "🌧️")  # rainy

    def test_cli_output(self):
        # Ensure the CLI prints something (not testing exact output)
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "src.forecast", "2025-01-01"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.stdout.strip())  # non‑empty

if __name__ == "__main__":
    unittest.main()
