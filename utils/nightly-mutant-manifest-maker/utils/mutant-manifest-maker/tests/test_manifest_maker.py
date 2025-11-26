import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add the src directory to the path to import manifest_maker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import manifest_maker

class TestManifestMaker(unittest.TestCase):

    # Mock rationale: We need to simulate a file system without actually creating files
    # on disk, ensuring tests are deterministic and offline.
    # os.walk is mocked to provide a predefined directory structure.
    # os.path.isdir is mocked to confirm the root directory exists.
    # os.path.getsize and os.path.getmtime are mocked to provide consistent metadata.
    # os.path.relpath is mocked to ensure consistent relative paths regardless of OS.
    # os.path.join is mocked to ensure consistent path joining regardless of OS.
    # os.path.abspath is mocked to provide a consistent absolute path for the root_dir.

    @patch('os.path.abspath', return_value='/mock/root')
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start + os.sep, ''))
    @patch('os.path.join', side_effect=os.path.join) # Use actual join for internal path construction
    def test_scan_directory_with_patterns(self, mock_join, mock_relpath, mock_getmtime, mock_getsize, mock_walk, mock_isdir, mock_abspath):
        # Define a mock file system structure
        mock_walk.return_value = [
            ('/mock/root', ['src', 'docs'], ['README.md', 'config.json']),
            ('/mock/root/src', [], ['main.py', 'helper.js']),
            ('/mock/root/docs', [], ['guide.md', 'images.txt']),
        ]

        # Define mock file metadata
        mock_getsize.side_effect = lambda p: {
            '/mock/root/README.md': 100,
            '/mock/root/config.json': 50,
            '/mock/root/src/main.py': 200,
            '/mock/root/src/helper.js': 150,
            '/mock/root/docs/guide.md': 300,
            '/mock/root/docs/images.txt': 25,
        }.get(p, 0)

        # Use a fixed timestamp for consistency
        fixed_timestamp = datetime(2023, 1, 1, 12, 0, 0).timestamp()
        mock_getmtime.return_value = fixed_timestamp

        root_dir = '/mock/root'
        include_patterns = ["*.py", "*.md"]

        entries = manifest_maker.scan_directory(root_dir, include_patterns)

        self.assertEqual(len(entries), 3)
        
        # Sort entries for consistent assertion
        entries.sort(key=lambda x: x['path'])

        self.assertEqual(entries[0]['path'], 'README.md')
        self.assertEqual(entries[0]['size'], 100)
        self.assertEqual(entries[0]['mtime'], '2023-01-01 12:00:00')

        self.assertEqual(entries[1]['path'], 'docs/guide.md')
        self.assertEqual(entries[1]['size'], 300)
        self.assertEqual(entries[1]['mtime'], '2023-01-01 12:00:00')

        self.assertEqual(entries[2]['path'], 'src/main.py')
        self.assertEqual(entries[2]['size'], 200)
        self.assertEqual(entries[2]['mtime'], '2023-01-01 12:00:00')

    @patch('os.path.abspath', return_value='/mock/root')
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start + os.sep, ''))
    @patch('os.path.join', side_effect=os.path.join)
    def test_scan_directory_no_patterns(self, mock_join, mock_relpath, mock_getmtime, mock_getsize, mock_walk, mock_isdir, mock_abspath):
        # Test with default pattern "*" (all files)
        mock_walk.return_value = [
            ('/mock/root', [], ['file1.txt', 'file2.log']),
        ]
        mock_getsize.side_effect = lambda p: {
            '/mock/root/file1.txt': 10,
            '/mock/root/file2.log': 20,
        }.get(p, 0)
        fixed_timestamp = datetime(2023, 1, 1, 12, 0, 0).timestamp()
        mock_getmtime.return_value = fixed_timestamp

        root_dir = '/mock/root'
        include_patterns = ["*"] # All files

        entries = manifest_maker.scan_directory(root_dir, include_patterns)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]['path'], 'file1.txt')
        self.assertEqual(entries[1]['path'], 'file2.log')

    @patch('os.path.isdir', return_value=False)
    def test_scan_directory_not_found(self, mock_isdir):
        with self.assertRaises(FileNotFoundError):
            manifest_maker.scan_directory('/nonexistent/path', ["*"])

    def test_generate_markdown_manifest(self):
        root_dir = '/test/project'
        manifest_entries = [
            {'path': 'src/main.py', 'size': 200, 'mtime': '2023-01-01 12:00:00'},
            {'path': 'README.md', 'size': 100, 'mtime': '2023-01-01 12:00:00'},
            {'path': 'docs/guide.md', 'size': 300, 'mtime': '2023-01-01 12:00:00'},
        ]
        
        # Mock abspath for consistent header
        with patch('os.path.abspath', return_value='/test/project'):
            markdown = manifest_maker.generate_markdown_manifest(root_dir, manifest_entries)

        expected_markdown = (
            "# Mutant Manifest for /test/project\n\n"
            "| File Path | Size (bytes) | Last Modified |\n"
            "|---|---|---|\n"
            "| README.md | 100 | 2023-01-01 12:00:00 |\n"
            "| docs/guide.md | 300 | 2023-01-01 12:00:00 |\n"
            "| src/main.py | 200 | 2023-01-01 12:00:00 |\n"
        )
        self.assertEqual(markdown, expected_markdown)

    @patch('sys.argv', ['manifest_maker.py', '/mock/root', '*.py', '*.md'])
    @patch('builtins.print')
    @patch('manifest_maker.scan_directory')
    @patch('manifest_maker.generate_markdown_manifest')
    @patch('os.path.abspath', return_value='/mock/root')
    def test_main_success(self, mock_abspath, mock_generate, mock_scan, mock_print):
        mock_scan.return_value = [{'path': 'file.py', 'size': 10, 'mtime': '2023-01-01 12:00:00'}]
        mock_generate.return_value = "Mock Markdown Output"

        manifest_maker.main()

        mock_scan.assert_called_once_with('/mock/root', ['*.py', '*.md'])
        mock_generate.assert_called_once() # Check arguments separately if needed
        mock_print.assert_called_once_with("Mock Markdown Output")

    @patch('sys.argv', ['manifest_maker.py', '/nonexistent/path'])
    @patch('builtins.print')
    @patch('sys.exit')
    @patch('manifest_maker.scan_directory', side_effect=FileNotFoundError("Directory not found"))
    def test_main_file_not_found_error(self, mock_scan, mock_exit, mock_print):
        manifest_maker.main()
        mock_print.assert_called_with("Error: Directory not found", file=sys.stderr)
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['manifest_maker.py'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_arguments(self, mock_exit, mock_print):
        manifest_maker.main()
        mock_print.assert_called_with("Usage: python src/manifest_maker.py <directory_to_scan> [pattern1] [pattern2] ...")
        mock_exit.assert_called_once_with(1)
