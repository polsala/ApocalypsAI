import unittest
from unittest.mock import patch, mock_open
import sys
import os

# Mock rationale: We need to test file system operations (reading/writing hosts file)
# and system-specific paths without actually touching the real file system or
# requiring root privileges during tests. `mock_open` and `patch` allow us to
# simulate these interactions.

# Mock rationale: We need to test the behavior of the script on different operating
# systems without actually changing the test environment's OS. `platform.system`
# is mocked to return specific OS names.

# Mock rationale: We need to capture and inspect the output printed to stdout/stderr
# by the utility functions without it polluting the test runner's console. `sys.stdout`
# and `sys.stderr` are mocked to redirect output to a string buffer.

# Mock rationale: We need to control the exit behavior of the script when errors occur
# without actually terminating the test suite. `sys.exit` is mocked to raise an
# exception instead of exiting.

# Import the functions to be tested
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import blocker

class TestDoomScrollBlocker(unittest.TestCase):

    def setUp(self):
        # Reset the hosts file content for each test
        self.mock_hosts_content = []
        self.mock_file_handle = mock_open(read_data=''.join(self.mock_hosts_content))
        self.mock_file_handle.return_value.readlines.side_effect = lambda: self.mock_hosts_content
        self.mock_file_handle.return_value.writelines.side_effect = lambda lines: self._update_mock_content(lines)
        self.mock_file_handle.return_value.write.side_effect = lambda data: self._update_mock_content([data])
        self.mock_file_handle.return_value.truncate.side_effect = lambda: None # Truncate does nothing in mock

        # Patch open for file operations
        self.patcher_open = patch('builtins.open', self.mock_file_handle)
        self.mock_open = self.patcher_open.start()

        # Patch platform.system for OS detection
        self.patcher_platform = patch('platform.system', return_value='Linux')
        self.mock_platform = self.patcher_platform.start()

        # Patch sys.exit to prevent actual exit during tests
        self.patcher_sys_exit = patch('sys.exit', side_effect=SystemExit)
        self.mock_sys_exit = self.patcher_sys_exit.start()

        # Capture stdout and stderr
        self.held_stdout = sys.stdout
        self.held_stderr = sys.stderr
        sys.stdout = self.mock_stdout = unittest.mock.StringIO()
        sys.stderr = self.mock_stderr = unittest.mock.StringIO()

    def tearDown(self):
        self.patcher_open.stop()
        self.patcher_platform.stop()
        self.patcher_sys_exit.stop()
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    def _update_mock_content(self, new_lines):
        # Simulate writing to the file by updating mock_hosts_content
        # This is a simplified simulation, assuming writes always replace content
        # after seek(0) and truncate().
        self.mock_hosts_content = []
        for line in new_lines:
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            self.mock_hosts_content.append(line)

    def test_get_hosts_file_path_linux(self):
        self.mock_platform.return_value = 'Linux'
        self.assertEqual(blocker.get_hosts_file_path(), '/etc/hosts')

    def test_get_hosts_file_path_windows(self):
        self.mock_platform.return_value = 'Windows'
        with patch.dict(os.environ, {'SystemRoot': 'C:\\Windows'}):
            self.assertEqual(blocker.get_hosts_file_path(), 'C:\\Windows\\System32\\drivers\\etc\\hosts')

    def test_block_sites_adds_entries(self):
        sites = ['example.com', 'news.org']
        blocker.block_sites(sites)

        expected_lines = [
            f"127.0.0.1 example.com {blocker.BLOCKER_MARKER}\n",
            f"127.0.0.1 news.org {blocker.BLOCKER_MARKER}\n"
        ]
        self.assertEqual(self.mock_hosts_content, expected_lines)
        self.assertIn("Successfully blocked", self.mock_stdout.getvalue())

    def test_block_sites_handles_existing_content(self):
        self.mock_hosts_content = [
            "127.0.0.1 localhost\n",
            "# Some other comment\n"
        ]
        sites = ['example.com']
        blocker.block_sites(sites)

        expected_lines = [
            "127.0.0.1 localhost\n",
            "# Some other comment\n",
            f"127.0.0.1 example.com {blocker.BLOCKER_MARKER}\n"
        ]
        self.assertEqual(self.mock_hosts_content, expected_lines)

    def test_block_sites_prevents_duplicates(self):
        self.mock_hosts_content = [
            f"127.0.0.1 example.com {blocker.BLOCKER_MARKER}\n"
        ]
        sites = ['example.com', 'news.org']
        blocker.block_sites(sites)

        expected_lines = [
            f"127.0.0.1 example.com {blocker.BLOCKER_MARKER}\n",
            f"127.0.0.1 news.org {blocker.BLOCKER_MARKER}\n"
        ]
        self.assertEqual(self.mock_hosts_content, expected_lines)

    def test_unblock_sites_removes_entries(self):
        self.mock_hosts_content = [
            "127.0.0.1 localhost\n",
            f"127.0.0.1 example.com {blocker.BLOCKER_MARKER}\n",
            f"127.0.0.1 news.org {blocker.BLOCKER_MARKER}\n",
            "# Another entry\n"
        ]
        blocker.unblock_sites()

        expected_lines = [
            "127.0.0.1 localhost\n",
            "# Another entry\n"
        ]
        self.assertEqual(self.mock_hosts_content, expected_lines)
        self.assertIn("Successfully unblocked", self.mock_stdout.getvalue())

    def test_unblock_sites_no_blocker_entries(self):
        self.mock_hosts_content = [
            "127.0.0.1 localhost\n",
            "# Another entry\n"
        ]
        blocker.unblock_sites()

        expected_lines = [
            "127.0.0.1 localhost\n",
            "# Another entry\n"
        ]
        self.assertEqual(self.mock_hosts_content, expected_lines)

    def test_block_sites_permission_error(self):
        self.mock_open.side_effect = PermissionError
        with self.assertRaises(SystemExit):
            blocker.block_sites(['example.com'])
        self.assertIn("Permission denied", self.mock_stderr.getvalue())

    def test_unblock_sites_permission_error(self):
        self.mock_open.side_effect = PermissionError
        with self.assertRaises(SystemExit):
            blocker.unblock_sites()
        self.assertIn("Permission denied", self.mock_stderr.getvalue())

    def test_block_sites_file_not_found(self):
        self.mock_open.side_effect = FileNotFoundError
        with self.assertRaises(SystemExit):
            blocker.block_sites(['example.com'])
        self.assertIn("Hosts file not found", self.mock_stderr.getvalue())

    def test_main_block_command(self):
        # Test main function with block command
        with patch('sys.argv', ['blocker.py', 'block', '--sites', 'test.com']):
            blocker.main()
            expected_lines = [f"127.0.0.1 test.com {blocker.BLOCKER_MARKER}\n"]
            self.assertEqual(self.mock_hosts_content, expected_lines)

    def test_main_unblock_command(self):
        # Setup some blocked sites first
        self.mock_hosts_content = [
            f"127.0.0.1 test.com {blocker.BLOCKER_MARKER}\n"
        ]
        with patch('sys.argv', ['blocker.py', 'unblock']):
            blocker.main()
            self.assertEqual(self.mock_hosts_content, [])

    def test_main_invalid_command(self):
        with patch('sys.argv', ['blocker.py', 'invalid']):
            with self.assertRaises(SystemExit):
                blocker.main()
            self.assertIn("Unknown command", self.mock_stderr.getvalue())

    def test_main_block_no_sites_arg(self):
        with patch('sys.argv', ['blocker.py', 'block']):
            with self.assertRaises(SystemExit):
                blocker.main()
            self.assertIn("'--sites' argument is required", self.mock_stderr.getvalue())

    def test_main_block_empty_sites(self):
        with patch('sys.argv', ['blocker.py', 'block', '--sites', '']):
            with self.assertRaises(SystemExit):
                blocker.main()
            self.assertIn("No sites provided for blocking", self.mock_stderr.getvalue())

    def test_main_block_malformed_sites_arg(self):
        with patch('sys.argv', ['blocker.py', 'block', '--sites']):
            with self.assertRaises(SystemExit):
                blocker.main()
            self.assertIn("Invalid '--sites' argument", self.mock_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
