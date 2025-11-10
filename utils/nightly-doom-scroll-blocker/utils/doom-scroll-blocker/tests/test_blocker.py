import unittest
from unittest.mock import patch, mock_open, call
import os
import sys

# Add the src directory to the path to allow importing blocker.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import blocker

class TestDoomScrollBlocker(unittest.TestCase):

    def setUp(self):
        # Reset sys.exit for each test
        self.patcher_sys_exit = patch('sys.exit')
        self.mock_sys_exit = self.patcher_sys_exit.start()
        self.mock_sys_exit.side_effect = SystemExit # Allow catching SystemExit

        # Patch print to suppress output during tests and capture if needed
        self.patcher_print = patch('builtins.print')
        self.mock_print = self.patcher_print.start()

    def tearDown(self):
        self.patcher_sys_exit.stop()
        self.patcher_print.stop()

    @patch('os.name', new='posix')
    def test_get_hosts_file_path_unix(self):
        # Mock rationale: os.name determines the hosts file path, so we mock it to simulate a Unix-like system.
        self.assertEqual(blocker.get_hosts_file_path(), '/etc/hosts')

    @patch('os.name', new='nt')
    def test_get_hosts_file_path_windows(self):
        # Mock rationale: os.name determines the hosts file path, so we mock it to simulate a Windows system.
        self.assertEqual(blocker.get_hosts_file_path(), r'C:\Windows\System32\drivers\etc\hosts')

    @patch('os.name', new='unsupported_os')
    def test_get_hosts_file_path_unsupported(self):
        # Mock rationale: os.name determines the hosts file path, so we mock it to simulate an unsupported OS.
        with self.assertRaises(OSError):
            blocker.get_hosts_file_path()

    @patch('builtins.open', new_callable=mock_open, read_data='site1.com\n#comment\nsite2.org\n')
    def test_load_blocked_sites_success(self, mock_file):
        # Mock rationale: We need to simulate reading the blocked_sites.txt file without actually touching the filesystem.
        sites = blocker.load_blocked_sites('dummy_path/blocked_sites.txt')
        self.assertEqual(sites, ['site1.com', 'site2.org'])
        mock_file.assert_called_once_with('dummy_path/blocked_sites.txt', 'r')

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_blocked_sites_file_not_found(self, mock_file):
        # Mock rationale: Simulate the scenario where blocked_sites.txt does not exist.
        with self.assertRaises(SystemExit) as cm:
            blocker.load_blocked_sites('non_existent_path/blocked_sites.txt')
        self.assertEqual(cm.exception.code, 1)
        self.mock_print.assert_called_with("Error: 'non_existent_path/blocked_sites.txt' not found. Please create it with sites to block.")

    @patch('builtins.open', new_callable=mock_open, read_data='127.0.0.1 localhost\n')
    def test_block_sites_success(self, mock_file):
        # Mock rationale: Simulate reading and writing to the hosts file without actual file operations.
        # We provide initial content and expect specific writes.
        mock_file.return_value.__enter__.return_value.readlines.return_value = ['127.0.0.1 localhost\n']
        sites_to_block = ['example.com', 'test.org']
        blocker.block_sites('/etc/hosts', sites_to_block)

        expected_write_calls = [
            call('127.0.0.1 localhost\n'),
            call('127.0.0.1\texample.com # ApocalypsAI Doom Scroll Blocker\n'),
            call('127.0.0.1\ttest.org # ApocalypsAI Doom Scroll Blocker\n')
        ]
        mock_file.return_value.__enter__.return_value.writelines.assert_has_calls(expected_write_calls, any_order=True)
        self.mock_print.assert_called_with('Successfully blocked 2 new sites. Total blocked by ApocalypsAI: 2.')

    @patch('builtins.open', new_callable=mock_open, read_data='127.0.0.1 localhost\n127.0.0.1 example.com # ApocalypsAI Doom Scroll Blocker\n')
    def test_block_sites_idempotency(self, mock_file):
        # Mock rationale: Test that blocking already blocked sites doesn't add duplicates.
        mock_file.return_value.__enter__.return_value.readlines.return_value = [
            '127.0.0.1 localhost\n',
            '127.0.0.1\texample.com # ApocalypsAI Doom Scroll Blocker\n'
        ]
        sites_to_block = ['example.com', 'newsite.net']
        blocker.block_sites('/etc/hosts', sites_to_block)

        expected_write_calls = [
            call('127.0.0.1 localhost\n'),
            call('127.0.0.1\texample.com # ApocalypsAI Doom Scroll Blocker\n'),
            call('127.0.0.1\tnewsite.net # ApocalypsAI Doom Scroll Blocker\n')
        ]
        mock_file.return_value.__enter__.return_value.writelines.assert_has_calls(expected_write_calls, any_order=True)
        self.mock_print.assert_called_with('Successfully blocked 1 new sites. Total blocked by ApocalypsAI: 2.')

    @patch('builtins.open', new_callable=mock_open, read_data='127.0.0.1 localhost\n')
    def test_block_sites_permission_error_read(self, mock_file):
        # Mock rationale: Simulate a PermissionError when trying to read the hosts file.
        mock_file.side_effect = PermissionError
        with self.assertRaises(SystemExit) as cm:
            blocker.block_sites('/etc/hosts', ['example.com'])
        self.assertEqual(cm.exception.code, 1)
        self.mock_print.assert_called_with("Error: Permission denied to read '/etc/hosts'. Run as administrator/root.")

    @patch('builtins.open', new_callable=mock_open)
    def test_block_sites_permission_error_write(self, mock_file):
        # Mock rationale: Simulate a PermissionError when trying to write to the hosts file.
        mock_file.return_value.__enter__.return_value.readlines.return_value = ['127.0.0.1 localhost\n']
        mock_file.return_value.__enter__.return_value.writelines.side_effect = PermissionError
        with self.assertRaises(SystemExit) as cm:
            blocker.block_sites('/etc/hosts', ['example.com'])
        self.assertEqual(cm.exception.code, 1)
        self.mock_print.assert_called_with("Error: Permission denied to write to '/etc/hosts'. Run as administrator/root.")

    @patch('builtins.open', new_callable=mock_open, read_data='127.0.0.1 localhost\n127.0.0.1 example.com # ApocalypsAI Doom Scroll Blocker\n127.0.0.1 test.org # ApocalypsAI Doom Scroll Blocker\n')
    def test_unblock_sites_success(self, mock_file):
        # Mock rationale: Simulate reading and writing to the hosts file to remove blocked entries.
        mock_file.return_value.__enter__.return_value.readlines.return_value = [
            '127.0.0.1 localhost\n',
            '127.0.0.1\texample.com # ApocalypsAI Doom Scroll Blocker\n',
            '127.0.0.1\ttest.org # ApocalypsAI Doom Scroll Blocker\n'
        ]
        blocker.unblock_sites('/etc/hosts')

        expected_write_calls = [
            call('127.0.0.1 localhost\n')
        ]
        mock_file.return_value.__enter__.return_value.writelines.assert_has_calls(expected_write_calls, any_order=True)
        self.mock_print.assert_called_with('Successfully unblocked 2 sites previously blocked by ApocalypsAI.')

    @patch('builtins.open', new_callable=mock_open, read_data='127.0.0.1 localhost\n')
    def test_unblock_sites_no_blocked_found(self, mock_file):
        # Mock rationale: Test unblocking when no sites were blocked by this utility.
        mock_file.return_value.__enter__.return_value.readlines.return_value = ['127.0.0.1 localhost\n']
        blocker.unblock_sites('/etc/hosts')
        # Ensure writelines was not called as no changes were made
        mock_file.return_value.__enter__.return_value.writelines.assert_not_called()
        self.mock_print.assert_called_with('No sites previously blocked by ApocalypsAI found in hosts file.')

    @patch('builtins.open', new_callable=mock_open)
    def test_unblock_sites_permission_error_write(self, mock_file):
        # Mock rationale: Simulate a PermissionError when trying to write to the hosts file during unblock.
        mock_file.return_value.__enter__.return_value.readlines.return_value = [
            '127.0.0.1 localhost\n',
            '127.0.0.1\texample.com # ApocalypsAI Doom Scroll Blocker\n'
        ]
        mock_file.return_value.__enter__.return_value.writelines.side_effect = PermissionError
        with self.assertRaises(SystemExit) as cm:
            blocker.unblock_sites('/etc/hosts')
        self.assertEqual(cm.exception.code, 1)
        self.mock_print.assert_called_with("Error: Permission denied to write to '/etc/hosts'. Run as administrator/root.")

    @patch('blocker.get_hosts_file_path', return_value='/etc/hosts')
    @patch('blocker.load_blocked_sites', return_value=['example.com'])
    @patch('blocker.block_sites')
    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(mode='block'))
    def test_main_block_mode(self, mock_parse_args, mock_block_sites, mock_load_sites, mock_get_path):
        # Mock rationale: Test the main function's flow for 'block' mode by mocking its dependencies.
        blocker.main()
        mock_get_path.assert_called_once()
        mock_load_sites.assert_called_once()
        mock_block_sites.assert_called_once_with('/etc/hosts', ['example.com'])

    @patch('blocker.get_hosts_file_path', return_value='/etc/hosts')
    @patch('blocker.unblock_sites')
    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(mode='unblock'))
    def test_main_unblock_mode(self, mock_parse_args, mock_unblock_sites, mock_get_path):
        # Mock rationale: Test the main function's flow for 'unblock' mode by mocking its dependencies.
        blocker.main()
        mock_get_path.assert_called_once()
        mock_unblock_sites.assert_called_once_with('/etc/hosts')

    @patch('blocker.get_hosts_file_path', return_value='/etc/hosts')
    @patch('blocker.load_blocked_sites', return_value=[])
    @patch('blocker.block_sites')
    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(mode='block'))
    def test_main_block_mode_no_sites_configured(self, mock_parse_args, mock_block_sites, mock_load_sites, mock_get_path):
        # Mock rationale: Test the main function's flow when no sites are configured to block.
        blocker.main()
        mock_get_path.assert_called_once()
        mock_load_sites.assert_called_once()
        mock_block_sites.assert_not_called()
        self.mock_print.assert_called_with("No sites configured to block in 'blocked_sites.txt'.")
