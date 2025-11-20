import unittest
from unittest.mock import patch, MagicMock
import io
import sys
import requests
from src.flare_sender import check_url, main

class TestFlareSender(unittest.TestCase):

    def setUp(self):
        # Capture stdout and stderr for testing print statements and error messages
        self.held_stdout = sys.stdout
        self.mock_stdout = io.StringIO()
        sys.stdout = self.mock_stdout
        self.held_stderr = sys.stderr
        self.mock_stderr = io.StringIO()
        sys.stderr = self.mock_stderr

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    def test_check_url_success(self):
        # Mock rationale: Simulate a successful HTTP GET request (200 OK) for a given session object.
        mock_session = MagicMock(spec=requests.Session)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.reason = 'OK'
        mock_session.get.return_value = mock_response

        status = check_url('http://example.com', mock_session)
        self.assertEqual(status, '[200 OK]')
        mock_session.get.assert_called_once_with('http://example.com', timeout=5, allow_redirects=True)

    def test_check_url_not_found(self):
        # Mock rationale: Simulate a 404 Not Found HTTP response for a given session object.
        mock_session = MagicMock(spec=requests.Session)
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = 'Not Found'
        mock_session.get.return_value = mock_response

        status = check_url('http://example.com/nonexistent', mock_session)
        self.assertEqual(status, '[404 Not Found]')
        mock_session.get.assert_called_once_with('http://example.com/nonexistent', timeout=5, allow_redirects=True)

    def test_check_url_server_error(self):
        # Mock rationale: Simulate a 500 Internal Server Error HTTP response for a given session object.
        mock_session = MagicMock(spec=requests.Session)
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.reason = 'Internal Server Error'
        mock_session.get.return_value = mock_response

        status = check_url('http://example.com/error', mock_session)
        self.assertEqual(status, '[500 Internal Server Error]')
        mock_session.get.assert_called_once_with('http://example.com/error', timeout=5, allow_redirects=True)

    def test_check_url_connection_error(self):
        # Mock rationale: Simulate a network connection error for a given session object.
        mock_session = MagicMock(spec=requests.Session)
        mock_session.get.side_effect = requests.exceptions.ConnectionError
        
        status = check_url('http://unreachable.com', mock_session)
        self.assertEqual(status, '[Connection Error]')
        mock_session.get.assert_called_once_with('http://unreachable.com', timeout=5, allow_redirects=True)

    def test_check_url_timeout_error(self):
        # Mock rationale: Simulate a request timeout error for a given session object.
        mock_session = MagicMock(spec=requests.Session)
        mock_session.get.side_effect = requests.exceptions.Timeout
        
        status = check_url('http://slow-server.com', mock_session)
        self.assertEqual(status, '[Timeout Error]')
        mock_session.get.assert_called_once_with('http://slow-server.com', timeout=5, allow_redirects=True)

    def test_check_url_generic_request_error(self):
        # Mock rationale: Simulate a generic requests exception for a given session object.
        mock_session = MagicMock(spec=requests.Session)
        mock_session.get.side_effect = requests.exceptions.RequestException('Generic error')
        
        status = check_url('http://problematic.com', mock_session)
        self.assertEqual(status, '[Request Error: Generic error]')
        mock_session.get.assert_called_once_with('http://problematic.com', timeout=5, allow_redirects=True)

    @patch('builtins.open', new_callable=MagicMock)
    @patch('requests.Session') # Patch requests.Session to ensure no real session is created
    @patch('src.flare_sender.check_url') # Patch check_url to control its return values
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during tests
    @patch('argparse.ArgumentParser.parse_args') # Mock parse_args to control CLI arguments
    def test_main_successful_scan(self, mock_parse_args, mock_exit, mock_check_url, MockSession, mock_open):
        # Mock rationale: Simulate reading a URL file and successful URL checks.
        # mock_parse_args: Provides the --urls argument to main().
        # mock_open: Provides a mock file object for reading URLs.
        # MockSession: Ensures no actual network calls by preventing real session creation.
        # mock_check_url: Controls the return value for each URL check, simulating different statuses.
        # mock_exit: Prevents the program from exiting prematurely during tests.

        mock_parse_args.return_value = MagicMock(urls='test_urls.txt')
        mock_file_content = "http://url1.com\nhttp://url2.com"
        mock_open.return_value.__enter__.return_value = io.StringIO(mock_file_content)

        mock_check_url.side_effect = ['[200 OK]', '[404 Not Found]']

        main()

        output = self.mock_stdout.getvalue()
        self.assertIn("Initiating signal flare scan for 2 URLs...", output)
        self.assertIn("Checking URL: http://url1.com ... [200 OK]", output)
        self.assertIn("Checking URL: http://url2.com ... [404 Not Found]", output)
        self.assertIn("Signal flare scan complete.", output)
        mock_exit.assert_not_called()
        mock_check_url.assert_any_call('http://url1.com', MockSession.return_value)
        mock_check_url.assert_any_call('http://url2.com', MockSession.return_value)
        MockSession.assert_called_once() # Ensure a session was attempted to be created

    @patch('builtins.open', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_file_not_found(self, mock_parse_args, mock_exit, mock_open):
        # Mock rationale: Simulate a FileNotFoundError when opening the URL file.
        # mock_parse_args: Provides the --urls argument.
        # mock_open: Raises FileNotFoundError.
        # mock_exit: Captures the exit call.

        mock_parse_args.return_value = MagicMock(urls='nonexistent.txt')
        mock_open.side_effect = FileNotFoundError

        main()

        output = self.mock_stderr.getvalue() # Error output goes to stderr
        self.assertIn("Error: URL file not found at 'nonexistent.txt'", output)
        mock_exit.assert_called_once_with(1)

    @patch('builtins.open', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_empty_file(self, mock_parse_args, mock_exit, mock_open):
        # Mock rationale: Simulate an empty URL file, leading to an early exit with status 0.
        # mock_parse_args: Provides the --urls argument.
        # mock_open: Returns an empty file content.
        # mock_exit: Captures the exit call.

        mock_parse_args.return_value = MagicMock(urls='empty.txt')
        mock_open.return_value.__enter__.return_value = io.StringIO("")

        main()

        output = self.mock_stdout.getvalue()
        self.assertIn("No URLs found in the provided file.", output)
        mock_exit.assert_called_once_with(0)

    @patch('builtins.open', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_file_read_error(self, mock_parse_args, mock_exit, mock_open):
        # Mock rationale: Simulate a generic IOError during file reading.
        # mock_parse_args: Provides the --urls argument.
        # mock_open: Raises IOError.
        # mock_exit: Captures the exit call.

        mock_parse_args.return_value = MagicMock(urls='protected.txt')
        mock_open.side_effect = IOError("Permission denied")

        main()

        output = self.mock_stderr.getvalue() # Error output goes to stderr
        self.assertIn("Error reading URL file: Permission denied", output)
        mock_exit.assert_called_once_with(1)
