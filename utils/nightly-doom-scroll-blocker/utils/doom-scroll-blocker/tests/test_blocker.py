import unittest
from unittest.mock import patch, mock_open
import sys
import os

# Mock rationale: We need to test file operations without actually touching the system's hosts file.
# `mock_open` allows us to simulate reading from and writing to a file in memory.
# `patch('os.name')` allows us to simulate different operating systems (Windows vs. Unix-like).
# `patch('sys.argv')` allows us to simulate command-line arguments passed to the script.
# `patch('sys.exit')` prevents the script from actually exiting during tests.
# `patch('builtins.print')` allows us to capture and assert on printed output.

# Import the functions from the script to be tested
# Note: Imports are done within test methods or after relevant patches if module-level execution depends on mocks.
# For `get_hosts_path`, we import it inside the test method to ensure `os.name` is patched first.

class TestDoomScrollBlocker(unittest.TestCase):

    def setUp(self):
        # Reset sys.argv before each test
        self._original_argv = sys.argv
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = self.stdout_mock = unittest.mock.StringIO()
        sys.stderr = self.stderr_mock = unittest.mock.StringIO()

    def tearDown(self):
        sys.argv = self._original_argv
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

    @patch('os.name', 'posix') # Mock rationale: Test Unix-like path
    def test_get_hosts_path_unix(self):
        from src.blocker import get_hosts_path, HOSTS_PATH_UNIX
        self.assertEqual(get_hosts_path(), HOSTS_PATH_UNIX)

    @patch('os.name', 'nt') # Mock rationale: Test Windows path
    def test_get_hosts_path_windows(self):
        from src.blocker import get_hosts_path, HOSTS_PATH_WINDOWS
        self.assertEqual(get_hosts_path(), HOSTS_PATH_WINDOWS)

    @patch('builtins.open', new_callable=mock_open, read_data='line1\nline2\n') # Mock rationale: Simulate reading a hosts file
    def test_read_hosts_success(self, mock_file):
        from src.blocker import read_hosts
        content = read_hosts('/fake/path')
        self.assertEqual(content, ['line1\n', 'line2\n'])
        mock_file.assert_called_once_with('/fake/path', 'r')

    @patch('builtins.open', side_effect=IOError('Permission denied')) # Mock rationale: Simulate permission error during read
    @patch('sys.exit', return_value=None) # Mock rationale: Prevent actual exit during test
    def test_read_hosts_io_error(self, mock_exit, mock_file):
        from src.blocker import read_hosts
        read_hosts('/fake/path')
        self.assertIn('Error reading hosts file', self.stderr_mock.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Simulate writing to a hosts file
    def test_write_hosts_success(self, mock_file):
        from src.blocker import write_hosts
        write_hosts('/fake/path', ['new_line1\n', 'new_line2\n'])
        mock_file.assert_called_once_with('/fake/path', 'w')
        mock_file().writelines.assert_called_once_with(['new_line1\n', 'new_line2\n'])

    @patch('builtins.open', side_effect=IOError('Permission denied')) # Mock rationale: Simulate permission error during write
    @patch('sys.exit', return_value=None) # Mock rationale: Prevent actual exit during test
    def test_write_hosts_io_error(self, mock_exit, mock_file):
        from src.blocker import write_hosts
        write_hosts('/fake/path', ['new_line1\n'])
        self.assertIn('Error writing to hosts file', self.stderr_mock.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('src.blocker.get_hosts_path', return_value='/fake/hosts') # Mock rationale: Control hosts file path
    @patch('builtins.open', new_callable=mock_open, read_data='127.0.0.1 localhost\n') # Mock rationale: Simulate initial hosts file content
    def test_block_sites(self, mock_file, mock_get_path):
        from src.blocker import block_sites, BLOCKER_START_MARKER, BLOCKER_END_MARKER
        sites_to_block = ['example.com', 'test.net']
        block_sites(sites_to_block)

        expected_write_content = [
            '127.0.0.1 localhost\n',
            f'{BLOCKER_START_MARKER}\n',
            '127.0.0.1 example.com\n',
            '127.0.0.1 www.example.com\n',
            '127.0.0.1 test.net\n',
            '127.0.0.1 www.test.net\n',
            f'{BLOCKER_END_MARKER}\n'
        ]
        mock_file().writelines.assert_called_once_with(expected_write_content)
        self.assertIn('Blocking example.com, test.net...', self.stdout_mock.getvalue())
        self.assertIn('Successfully updated hosts file.', self.stdout_mock.getvalue())

    @patch('src.blocker.get_hosts_path', return_value='/fake/hosts') # Mock rationale: Control hosts file path
    @patch('builtins.open', new_callable=mock_open, read_data='127.0.0.1 localhost\n' \
                                                              f'{BLOCKER_START_MARKER}\n' \
                                                              '127.0.0.1 example.com\n' \
                                                              '127.0.0.1 www.example.com\n' \
                                                              f'{BLOCKER_END_MARKER}\n') # Mock rationale: Simulate hosts file with blocked entries
    def test_unblock_sites(self, mock_file, mock_get_path):
        from src.blocker import unblock_sites
        unblock_sites()

        expected_write_content = [
            '127.0.0.1 localhost\n'
        ]
        mock_file().writelines.assert_called_once_with(expected_write_content)
        self.assertIn('Unblocking websites...', self.stdout_mock.getvalue())
        self.assertIn('Successfully restored hosts file.', self.stdout_mock.getvalue())

    @patch('src.blocker.get_hosts_path', return_value='/fake/hosts') # Mock rationale: Control hosts file path
    @patch('builtins.open', new_callable=mock_open, read_data='127.0.0.1 localhost\n' \
                                                              f'{BLOCKER_START_MARKER}\n' \
                                                              '127.0.0.1 old.com\n' \
                                                              f'{BLOCKER_END_MARKER}\n') # Mock rationale: Simulate hosts file with existing blocked entries
    def test_block_sites_replaces_existing(self, mock_file, mock_get_path):
        from src.blocker import block_sites, BLOCKER_START_MARKER, BLOCKER_END_MARKER
        sites_to_block = ['newsite.com']
        block_sites(sites_to_block)

        expected_write_content = [
            '127.0.0.1 localhost\n',
            f'{BLOCKER_START_MARKER}\n',
            '127.0.0.1 newsite.com\n',
            '127.0.0.1 www.newsite.com\n',
            f'{BLOCKER_END_MARKER}\n'
        ]
        mock_file().writelines.assert_called_once_with(expected_write_content)

    @patch('sys.argv', ['blocker.py', 'start', 'site1.com', 'site2.org']) # Mock rationale: Simulate 'start' command with arguments
    @patch('src.blocker.block_sites') # Mock rationale: Isolate main function from actual blocking logic
    @patch('src.blocker.unblock_sites') # Mock rationale: Ensure unblock is not called
    def test_main_start_command(self, mock_unblock, mock_block):
        from src.blocker import main
        main()
        mock_block.assert_called_once_with(['site1.com', 'site2.org'])
        mock_unblock.assert_not_called()

    @patch('sys.argv', ['blocker.py', 'stop']) # Mock rationale: Simulate 'stop' command
    @patch('src.blocker.block_sites') # Mock rationale: Ensure block is not called
    @patch('src.blocker.unblock_sites') # Mock rationale: Isolate main function from actual unblocking logic
    def test_main_stop_command(self, mock_unblock, mock_block):
        from src.blocker import main
        main()
        mock_unblock.assert_called_once()
        mock_block.assert_not_called()

    @patch('sys.argv', ['blocker.py']) # Mock rationale: Simulate no arguments
    @patch('sys.exit', return_value=None) # Mock rationale: Prevent actual exit during test
    @patch('src.blocker.block_sites')
    @patch('src.blocker.unblock_sites')
    def test_main_no_command(self, mock_unblock, mock_block, mock_exit):
        from src.blocker import main
        main()
        self.assertIn('Usage: python blocker.py start <site1> [site2...] | stop', self.stderr_mock.getvalue())
        mock_exit.assert_called_once_with(1)
        mock_block.assert_not_called()
        mock_unblock.assert_not_called()

    @patch('sys.argv', ['blocker.py', 'start']) # Mock rationale: Simulate 'start' command without sites
    @patch('sys.exit', return_value=None) # Mock rationale: Prevent actual exit during test
    @patch('src.blocker.block_sites')
    def test_main_start_no_sites(self, mock_block, mock_exit):
        from src.blocker import main
        main()
        self.assertIn('Usage: python blocker.py start <site1> [site2...]', self.stderr_mock.getvalue())
        mock_exit.assert_called_once_with(1)
        mock_block.assert_not_called()

    @patch('sys.argv', ['blocker.py', 'unknown_command']) # Mock rationale: Simulate unknown command
    @patch('sys.exit', return_value=None) # Mock rationale: Prevent actual exit during test
    def test_main_unknown_command(self, mock_exit):
        from src.blocker import main
        main()
        self.assertIn('Unknown command: unknown_command', self.stderr_mock.getvalue())
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
