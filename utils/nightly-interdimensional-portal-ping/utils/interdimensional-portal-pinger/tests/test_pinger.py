import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import io
import os

# Mock rationale: We need to test the pinger's logic without making actual network requests
# or touching the filesystem. Mocking `requests.get` allows simulating various network
# responses (success, connection error, timeout). Mocking `open` allows simulating the
# presence or absence of the `portals.txt` file and its content. Mocking `os.path` functions
# ensures deterministic path resolution independent of the test environment.

# Add the src directory to the path for importing pinger
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pinger
sys.path.pop(0)

class TestInterdimensionalPortalPinger(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        self.new_stdout = io.StringIO()
        sys.stdout = self.new_stdout

        # Capture stderr for testing error messages
        self.held_stderr = sys.stderr
        self.new_stderr = io.StringIO()
        sys.stderr = self.new_stderr

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='http://portal1.com\nhttps://portal2.org\n# A comment\n  \nhttp://portal3.net')
    def test_read_portals_success(self, mock_file, mock_exists):
        portals = pinger.read_portals('portals.txt')
        self.assertEqual(portals, ['http://portal1.com', 'https://portal2.org', 'http://portal3.net'])
        mock_exists.assert_called_once_with('portals.txt')
        mock_file.assert_called_once_with('portals.txt', 'r')

    @patch('os.path.exists', return_value=False)
    def test_read_portals_file_not_found(self, mock_exists):
        portals = pinger.read_portals('non_existent.txt')
        self.assertEqual(portals, [])
        self.assertIn("Error: Portal file 'non_existent.txt' not found.", self.new_stderr.getvalue())
        mock_exists.assert_called_once_with('non_existent.txt')

    @patch('builtins.open', side_effect=IOError('Permission denied'))
    @patch('os.path.exists', return_value=True)
    def test_read_portals_io_error(self, mock_exists, mock_file):
        portals = pinger.read_portals('portals.txt')
        self.assertEqual(portals, [])
        self.assertIn("Error reading portal file 'portals.txt': Permission denied", self.new_stderr.getvalue())

    @patch('requests.get')
    def test_ping_portal_online(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        status = pinger.ping_portal('http://online.com')
        self.assertEqual(status, 'ONLINE (Status: 200)')
        mock_get.assert_called_once_with('http://online.com', timeout=pinger.DEFAULT_TIMEOUT)

    @patch('requests.get')
    def test_ping_portal_online_non_200(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        status = pinger.ping_portal('http://notfound.com')
        self.assertEqual(status, 'ONLINE (Status: 404) - Non-200')
        mock_get.assert_called_once_with('http://notfound.com', timeout=pinger.DEFAULT_TIMEOUT)

    @patch('requests.get', side_effect=requests.exceptions.ConnectionError)
    def test_ping_portal_offline(self, mock_get):
        status = pinger.ping_portal('http://offline.com')
        self.assertEqual(status, 'OFFLINE (Connection Error)')
        mock_get.assert_called_once_with('http://offline.com', timeout=pinger.DEFAULT_TIMEOUT)

    @patch('requests.get', side_effect=requests.exceptions.Timeout)
    def test_ping_portal_timeout(self, mock_get):
        status = pinger.ping_portal('http://timeout.com')
        self.assertEqual(status, 'UNKNOWN_ERROR (Request Timeout)')
        mock_get.assert_called_once_with('http://timeout.com', timeout=pinger.DEFAULT_TIMEOUT)

    @patch('requests.get', side_effect=requests.exceptions.RequestException('Generic error'))
    def test_ping_portal_request_exception(self, mock_get):
        status = pinger.ping_portal('http://error.com')
        self.assertEqual(status, 'UNKNOWN_ERROR (RequestException)')
        mock_get.assert_called_once_with('http://error.com', timeout=pinger.DEFAULT_TIMEOUT)

    @patch('requests.get', side_effect=ValueError('Unexpected error'))
    def test_ping_portal_critical_error(self, mock_get):
        status = pinger.ping_portal('http://critical.com')
        self.assertEqual(status, 'CRITICAL_ERROR (ValueError)')
        mock_get.assert_called_once_with('http://critical.com', timeout=pinger.DEFAULT_TIMEOUT)

    @patch('pinger.read_portals', return_value=['http://mock-online.com', 'http://mock-offline.com'])
    @patch('pinger.ping_portal')
    @patch('os.path.dirname', return_value='/mock/path') # Mock os.path.dirname to control script_dir
    @patch('os.path.abspath', return_value='/mock/path/src/pinger.py') # Mock os.path.abspath for __file__
    @patch('os.path.join', side_effect=os.path.join) # Use real os.path.join for path construction with mocked components
    def test_main_integration(self, mock_join, mock_abspath, mock_dirname, mock_ping_portal, mock_read_portals):
        # Configure mock_ping_portal to return different statuses
        mock_ping_portal.side_effect = [
            'ONLINE (Status: 200)',
            'OFFLINE (Connection Error)'
        ]

        pinger.main()

        output = self.new_stdout.getvalue()
        self.assertIn('🌌 Initiating Interdimensional Portal Ping... 🌌', output)
        self.assertIn('[http://mock-online.com] - ONLINE (Status: 200)', output)
        self.assertIn('[http://mock-offline.com] - OFFLINE (Connection Error)', output)
        self.assertIn('🌌 Interdimensional Scan Complete. 🌌', output)

        # Verify read_portals was called with the correct, mocked path
        expected_portals_filepath = os.path.join('/mock/path', pinger.PORTALS_FILE)
        mock_read_portals.assert_called_once_with(expected_portals_filepath)

        self.assertEqual(mock_ping_portal.call_count, 2)
        mock_ping_portal.assert_any_call('http://mock-online.com')
        mock_ping_portal.assert_any_call('http://mock-offline.com')

    @patch('pinger.read_portals', return_value=[])
    @patch('os.path.dirname', return_value='/mock/path')
    @patch('os.path.abspath', return_value='/mock/path/src/pinger.py')
    @patch('os.path.join', side_effect=os.path.join)
    def test_main_no_portals(self, mock_join, mock_abspath, mock_dirname, mock_read_portals):
        pinger.main()
        output = self.new_stdout.getvalue()
        self.assertIn('No portals found to ping. Exiting.', output)
        mock_read_portals.assert_called_once_with(os.path.join('/mock/path', pinger.PORTALS_FILE))

if __name__ == '__main__':
    unittest.main()
