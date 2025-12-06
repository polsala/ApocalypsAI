import unittest
from unittest.mock import patch, mock_open
import os
from src import summarizer

class TestSummarizer(unittest.TestCase):

    # Mock rationale: We need to simulate file system operations (reading files, listing directories)
    # without actually touching the disk. This ensures tests are fast, deterministic, and isolated
    # from the environment.

    def setUp(self):
        self.default_keywords = ['ERROR', 'WARNING', 'INFO']

    @patch('builtins.open', new_callable=mock_open)
    def test_count_keywords_in_single_file(self, mock_file_open):
        mock_file_open.return_value.read.return_value = (
            "INFO: System started.\n"
            "ERROR: Disk full.\n"
            "WARNING: Low memory.\n"
            "info: User logged in.\n"
            "Error: Network issue.\n"
            "Another line with no keywords.\n"
        )
        filepath = '/mock/path/test.log'
        keywords = ['ERROR', 'WARNING', 'INFO']
        counts = summarizer.count_keywords_in_file(filepath, keywords)

        self.assertEqual(counts['ERROR'], 2)
        self.assertEqual(counts['WARNING'], 1)
        self.assertEqual(counts['INFO'], 2)
        mock_file_open.assert_called_once_with(filepath, 'r', encoding='utf-8', errors='ignore')

    @patch('builtins.open', new_callable=mock_open)
    def test_count_keywords_no_matches(self, mock_file_open):
        mock_file_open.return_value.read.return_value = (
            "Debug: This is a debug message.\n"
            "Trace: Another trace event.\n"
        )
        filepath = '/mock/path/no_match.log'
        keywords = ['ERROR', 'WARNING']
        counts = summarizer.count_keywords_in_file(filepath, keywords)

        self.assertEqual(counts.get('ERROR', 0), 0)
        self.assertEqual(counts.get('WARNING', 0), 0)
        mock_file_open.assert_called_once_with(filepath, 'r', encoding='utf-8', errors='ignore')

    @patch('builtins.open', new_callable=mock_open)
    def test_count_keywords_empty_file(self, mock_file_open):
        mock_file_open.return_value.read.return_value = ""
        filepath = '/mock/path/empty.log'
        keywords = ['ERROR']
        counts = summarizer.count_keywords_in_file(filepath, keywords)

        self.assertEqual(counts.get('ERROR', 0), 0)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_directory_with_multiple_files(self, mock_file_open, mock_os_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with multiple log files and their contents.
        # `os.walk` is mocked to yield specific directory/file lists.
        # `open` is mocked to return different content based on the filename.

        mock_os_walk.return_value = [
            ('/mock_dir', [], ['app.log', 'server.log', 'data.txt'])
        ]

        file_contents = {
            '/mock_dir/app.log': (
                "INFO: App started.\n"
                "ERROR: App crashed.\n"
                "WARNING: High CPU.\n"
            ),
            '/mock_dir/server.log': (
                "ERROR: Server down.\n"
                "ERROR: Server restart failed.\n"
                "INFO: Server up.\n"
            ),
            '/mock_dir/data.txt': (
                "This is not a log file.\n"
                "It should be ignored by default pattern.\n"
            )
        }

        def mock_open_side_effect(filepath, mode='r', encoding='utf-8', errors='ignore'):
            if filepath in file_contents:
                m = mock_open(read_data=file_contents[filepath])
                return m()
            raise FileNotFoundError(f"No such file: {filepath}")

        mock_file_open.side_effect = mock_open_side_effect

        directory = '/mock_dir'
        keywords = ['ERROR', 'WARNING', 'INFO']
        results = summarizer.scan_directory_for_logs(directory, keywords, file_pattern='*.log')

        self.assertIn('/mock_dir/app.log', results['files'])
        self.assertIn('/mock_dir/server.log', results['files'])
        self.assertNotIn('/mock_dir/data.txt', results['files']) # Should be filtered by pattern

        self.assertEqual(results['files']['/mock_dir/app.log']['ERROR'], 1)
        self.assertEqual(results['files']['/mock_dir/app.log']['WARNING'], 1)
        self.assertEqual(results['files']['/mock_dir/app.log']['INFO'], 1)

        self.assertEqual(results['files']['/mock_dir/server.log']['ERROR'], 2)
        self.assertEqual(results['files']['/mock_dir/server.log']['WARNING'], 0)
        self.assertEqual(results['files']['/mock_dir/server.log']['INFO'], 1)

        self.assertEqual(results['overall_totals']['ERROR'], 3)
        self.assertEqual(results['overall_totals']['WARNING'], 1)
        self.assertEqual(results['overall_totals']['INFO'], 2)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/mock_dir', [], ['report.txt', 'image.jpg'])])
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_directory_no_matching_files(self, mock_file_open, mock_os_walk, mock_isdir):
        # Mock rationale: Simulate a directory with files that do not match the default '*.log' pattern.
        directory = '/mock_dir'
        keywords = ['ERROR']
        results = summarizer.scan_directory_for_logs(directory, keywords)

        self.assertFalse(results['files'])
        self.assertFalse(results['overall_totals'])
        mock_file_open.assert_not_called()

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/mock_dir', [], ['custom.log', 'another.log'])])
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_directory_custom_file_pattern(self, mock_file_open, mock_os_walk, mock_isdir):
        # Mock rationale: Test that the utility correctly applies a custom file pattern.
        file_contents = {
            '/mock_dir/custom.log': 'ERROR: Custom log error.',
            '/mock_dir/another.log': 'WARNING: Another log warning.'
        }
        mock_file_open.side_effect = lambda f, *args, **kwargs: mock_open(read_data=file_contents[f])()

        directory = '/mock_dir'
        keywords = ['ERROR', 'WARNING']
        results = summarizer.scan_directory_for_logs(directory, keywords, file_pattern='*.log')

        self.assertIn('/mock_dir/custom.log', results['files'])
        self.assertIn('/mock_dir/another.log', results['files'])
        self.assertEqual(results['overall_totals']['ERROR'], 1)
        self.assertEqual(results['overall_totals']['WARNING'], 1)

    @patch('os.path.isdir', return_value=False)
    def test_scan_directory_non_existent_directory(self, mock_isdir):
        # Mock rationale: Ensure the utility handles cases where the specified directory does not exist.
        with self.assertRaises(ValueError) as cm:
            summarizer.scan_directory_for_logs('/non_existent', self.default_keywords)
        self.assertIn("Directory not found", str(cm.exception))

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/mock_dir', [], ['log1.txt'])])
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_directory_with_subdir(self, mock_file_open, mock_os_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with a subdirectory containing log files.
        mock_os_walk.return_value = [
            ('/mock_dir', ['subdir'], ['root.log']),
            ('/mock_dir/subdir', [], ['sub.log'])
        ]

        file_contents = {
            '/mock_dir/root.log': 'ERROR: Root log error.',
            '/mock_dir/subdir/sub.log': 'WARNING: Sub log warning.'
        }
        mock_file_open.side_effect = lambda f, *args, **kwargs: mock_open(read_data=file_contents[f])()

        directory = '/mock_dir'
        keywords = ['ERROR', 'WARNING']
        results = summarizer.scan_directory_for_logs(directory, keywords, file_pattern='*.log')

        self.assertIn('/mock_dir/root.log', results['files'])
        self.assertIn('/mock_dir/subdir/sub.log', results['files'])
        self.assertEqual(results['overall_totals']['ERROR'], 1)
        self.assertEqual(results['overall_totals']['WARNING'], 1)

if __name__ == '__main__':
    unittest.main()
