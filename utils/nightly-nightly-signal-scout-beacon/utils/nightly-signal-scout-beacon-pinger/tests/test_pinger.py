import unittest
from unittest.mock import patch, Mock
import sys
import io
import requests
from src.pinger import check_beacon, main

class TestPinger(unittest.TestCase):

    @patch('requests.get')
    def test_check_beacon_up(self, mock_get):
        # Mock rationale: Simulate a successful HTTP 200 response from a beacon.
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = check_beacon("http://example.com")
        self.assertEqual(result["url"], "http://example.com")
        self.assertEqual(result["status"], "UP")
        self.assertEqual(result["status_code"], 200)
        self.assertIsNone(result["error"])
        mock_get.assert_called_once_with("http://example.com", timeout=5)

    @patch('requests.get')
    def test_check_beacon_down_http_error(self, mock_get):
        # Mock rationale: Simulate an HTTP 404 error response from a beacon.
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = check_beacon("http://example.com/notfound")
        self.assertEqual(result["url"], "http://example.com/notfound")
        self.assertEqual(result["status"], "DOWN")
        self.assertEqual(result["status_code"], 404)
        self.assertIn("HTTP Error: 404", result["error"])

    @patch('requests.get')
    def test_check_beacon_down_timeout(self, mock_get):
        # Mock rationale: Simulate a network timeout when trying to reach a beacon.
        mock_get.side_effect = requests.exceptions.Timeout

        result = check_beacon("http://example.com/slow")
        self.assertEqual(result["url"], "http://example.com/slow")
        self.assertEqual(result["status"], "DOWN")
        self.assertIsNone(result["status_code"])
        self.assertEqual(result["error"], "Timeout")

    @patch('requests.get')
    def test_check_beacon_down_connection_error(self, mock_get):
        # Mock rationale: Simulate a general connection error (e.g., DNS failure, host unreachable).
        mock_get.side_effect = requests.exceptions.ConnectionError

        result = check_beacon("http://nonexistent.domain")
        self.assertEqual(result["url"], "http://nonexistent.domain")
        self.assertEqual(result["status"], "DOWN")
        self.assertIsNone(result["status_code"])
        self.assertEqual(result["error"], "Connection Error")

    @patch('requests.get')
    def test_check_beacon_down_generic_request_error(self, mock_get):
        # Mock rationale: Simulate an unexpected requests library error.
        mock_get.side_effect = requests.exceptions.RequestException("Something went wrong")

        result = check_beacon("http://example.com/error")
        self.assertEqual(result["url"], "http://example.com/error")
        self.assertEqual(result["status"], "DOWN")
        self.assertIsNone(result["status_code"])
        self.assertIn("Request Error: Something went wrong", result["error"])

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('src.pinger.check_beacon')
    def test_main_all_up(self, mock_check_beacon, mock_exit, mock_stdout):
        # Mock rationale: Simulate all beacons being 'UP' to test the main function's success path.
        mock_check_beacon.side_effect = [
            {"url": "http://beacon1.com", "status": "UP", "status_code": 200, "error": None},
            {"url": "http://beacon2.com", "status": "UP", "status_code": 200, "error": None},
        ]
        main(["http://beacon1.com", "http://beacon2.com"])
        self.assertIn("[UP] http://beacon1.com (HTTP 200)", mock_stdout.getvalue())
        self.assertIn("[UP] http://beacon2.com (HTTP 200)", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(0) # Expect success exit code

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('src.pinger.check_beacon')
    def test_main_some_down(self, mock_check_beacon, mock_exit, mock_stdout):
        # Mock rationale: Simulate one beacon being 'DOWN' to test the main function's failure path.
        mock_check_beacon.side_effect = [
            {"url": "http://beacon1.com", "status": "UP", "status_code": 200, "error": None},
            {"url": "http://beacon2.com", "status": "DOWN", "status_code": None, "error": "Timeout"},
        ]
        main(["http://beacon1.com", "http://beacon2.com"])
        self.assertIn("[UP] http://beacon1.com (HTTP 200)", mock_stdout.getvalue())
        self.assertIn("[DOWN] http://beacon2.com (Timeout)", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1) # Expect failure exit code

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_no_urls(self, mock_exit, mock_stdout):
        # Mock rationale: Test the scenario where no URLs are provided to the main function.
        main([])
        self.assertIn("No beacon URLs provided to check.", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(2) # Expect no-op exit code

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['pinger.py']) # Mock sys.argv for direct script execution
    def test_script_no_args(self, mock_exit, mock_stdout):
        # Mock rationale: Simulate running the script directly without any command-line arguments.
        with self.assertRaises(SystemExit) as cm:
            # Temporarily import the module to trigger __main__ block
            import importlib
            import src.pinger
            importlib.reload(src.pinger) # Reload to re-run __main__
        self.assertEqual(cm.exception.code, 2)
        self.assertIn("Usage: python pinger.py <url1> [url2] ...", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('src.pinger.check_beacon')
    @patch('sys.argv', ['pinger.py', 'http://test.com']) # Mock sys.argv for direct script execution
    def test_script_with_args(self, mock_check_beacon, mock_exit, mock_stdout):
        # Mock rationale: Simulate running the script directly with command-line arguments.
        mock_check_beacon.return_value = {"url": "http://test.com", "status": "UP", "status_code": 200, "error": None}
        with self.assertRaises(SystemExit) as cm:
            import importlib
            import src.pinger
            importlib.reload(src.pinger)
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("[UP] http://test.com (HTTP 200)", mock_stdout.getvalue())
        mock_check_beacon.assert_called_once_with("http://test.com")
