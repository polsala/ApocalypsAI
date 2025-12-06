import unittest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Import the function to be tested
from src.scanner import scan_directory, main

class TestScavengerScrutinyScanner(unittest.TestCase):

    # Mock rationale: os.walk interacts with the file system, which is non-deterministic
    # and slow for tests. Mocking it allows us to simulate a consistent file system
    # structure in memory for fast, reliable, and isolated testing.
    @patch('os.walk')
    @patch('pathlib.Path.is_dir')
    def test_scan_directory_by_extensions(self, mock_is_dir, mock_os_walk):
        mock_is_dir.return_value = True
        # Simulate a directory structure
        mock_os_walk.return_value = [
            ('/mock/root', [], ['file1.txt', 'document.pdf', 'image.jpg', 'notes.md']),
            ('/mock/root/subdir', [], ['report.csv', 'data.json', 'config.yml', 'another.txt']),
            ('/mock/root/empty', [], []),
        ]

        root = Path('/mock/root')
        extensions = {'.txt', '.md'}
        keywords = set()

        found = scan_directory(root, extensions, keywords)
        expected = {
            Path('/mock/root/file1.txt'),
            Path('/mock/root/notes.md'),
            Path('/mock/root/subdir/another.txt'),
        }
        self.assertEqual(set(found), expected)

    # Mock rationale: os.walk interacts with the file system, which is non-deterministic
    # and slow for tests. Mocking it allows us to simulate a consistent file system
    # structure in memory for fast, reliable, and isolated testing.
    @patch('os.walk')
    @patch('pathlib.Path.is_dir')
    def test_scan_directory_by_keywords(self, mock_is_dir, mock_os_walk):
        mock_is_dir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/root', [], ['config.ini', 'report_2023.pdf', 'image.jpg', 'my_notes.txt']),
            ('/mock/root/data', [], ['backup_db.sql', 'important_data.csv', 'temp.log']),
        ]

        root = Path('/mock/root')
        extensions = set()
        keywords = {'config', 'backup', 'notes'}

        found = scan_directory(root, extensions, keywords)
        expected = {
            Path('/mock/root/config.ini'),
            Path('/mock/root/my_notes.txt'),
            Path('/mock/root/data/backup_db.sql'),
        }
        self.assertEqual(set(found), expected)

    # Mock rationale: os.walk interacts with the file system, which is non-deterministic
    # and slow for tests. Mocking it allows us to simulate a consistent file system
    # structure in memory for fast, reliable, and isolated testing.
    @patch('os.walk')
    @patch('pathlib.Path.is_dir')
    def test_scan_directory_by_both_extensions_and_keywords(self, mock_is_dir, mock_os_walk):
        mock_is_dir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/root', [], ['config.json', 'report.txt', 'old_data.csv', 'important_notes.md']),
            ('/mock/root/archive', [], ['backup.zip', 'log_file.txt', 'my_plan.pdf']),
        ]

        root = Path('/mock/root')
        extensions = {'.txt', '.md'}
        keywords = {'config', 'important', 'plan'}

        found = scan_directory(root, extensions, keywords)
        expected = {
            Path('/mock/root/config.json'), # Matches keyword 'config'
            Path('/mock/root/report.txt'),  # Matches extension '.txt'
            Path('/mock/root/important_notes.md'), # Matches keyword 'important' AND extension '.md'
            Path('/mock/root/archive/log_file.txt'), # Matches extension '.txt'
            Path('/mock/root/archive/my_plan.pdf'), # Matches keyword 'plan'
        }
        self.assertEqual(set(found), expected)

    # Mock rationale: os.walk interacts with the file system, which is non-deterministic
    # and slow for tests. Mocking it allows us to simulate a consistent file system
    # structure in memory for fast, reliable, and isolated testing.
    @patch('os.walk')
    @patch('pathlib.Path.is_dir')
    def test_scan_directory_no_matches(self, mock_is_dir, mock_os_walk):
        mock_is_dir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/root', [], ['file.doc', 'image.png']),
        ]

        root = Path('/mock/root')
        extensions = {'.txt'}
        keywords = {'secret'}

        found = scan_directory(root, extensions, keywords)
        self.assertEqual(len(found), 0)

    # Mock rationale: os.walk interacts with the file system, which is non-deterministic
    # and slow for tests. Mocking it allows us to simulate a consistent file system
    # structure in memory for fast, reliable, and isolated testing.
    @patch('os.walk')
    @patch('pathlib.Path.is_dir')
    def test_scan_directory_empty_directory(self, mock_is_dir, mock_os_walk):
        mock_is_dir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/root', [], []),
        ]

        root = Path('/mock/root')
        extensions = {'.txt'}
        keywords = {'data'}

        found = scan_directory(root, extensions, keywords)
        self.assertEqual(len(found), 0)

    # Mock rationale: os.walk interacts with the file system, which is non-deterministic
    # and slow for tests. Mocking it allows us to simulate a consistent file system
    # structure in memory for fast, reliable, and isolated testing.
    @patch('os.walk')
    @patch('pathlib.Path.is_dir')
    def test_scan_directory_no_filters_all_files(self, mock_is_dir, mock_os_walk):
        mock_is_dir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/root', [], ['file1.txt', 'file2.pdf']),
            ('/mock/root/subdir', [], ['file3.json']),
        ]

        root = Path('/mock/root')
        extensions = set()
        keywords = set()

        found = scan_directory(root, extensions, keywords)
        expected = {
            Path('/mock/root/file1.txt'),
            Path('/mock/root/file2.pdf'),
            Path('/mock/root/subdir/file3.json'),
        }
        self.assertEqual(set(found), expected)

    # Mock rationale: pathlib.Path.is_dir interacts with the file system.
    # Mocking it allows us to test error handling for invalid paths without
    # needing to create actual directories.
    @patch('pathlib.Path.is_dir')
    def test_scan_directory_invalid_path(self, mock_is_dir):
        mock_is_dir.return_value = False # Simulate path is not a directory

        root = Path('/nonexistent/path')
        extensions = {'.txt'}
        keywords = set()

        # Capture stdout to check error message
        captured_output = StringIO()
        sys.stdout = captured_output
        found = scan_directory(root, extensions, keywords)
        sys.stdout = sys.__stdout__ # Reset stdout

        self.assertEqual(len(found), 0)
        self.assertIn("Error: Path '/nonexistent/path' is not a valid directory.", captured_output.getvalue())

    # Mock rationale: argparse.ArgumentParser.parse_args reads command-line arguments.
    # Mocking it allows us to programmatically provide arguments for testing the main function
    # without actually running the script from the command line.
    # Mock rationale: os.walk interacts with the file system, which is non-deterministic
    # and slow for tests. Mocking it allows us to simulate a consistent file system
    # structure in memory for fast, reliable, and isolated testing.
    @patch('sys.stdout', new_callable=StringIO)
    @patch('os.walk')
    @patch('pathlib.Path.is_dir')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_with_args(self, mock_parse_args, mock_is_dir, mock_os_walk, mock_stdout):
        mock_is_dir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/test_dir', [], ['report.txt', 'config.json', 'image.jpg', 'notes.md']),
        ]
        mock_parse_args.return_value = MagicMock(
            path='/mock/test_dir',
            extensions=['.txt', '.md'],
            keywords=['config']
        )

        main()
        output = mock_stdout.getvalue()

        self.assertIn("--- Found Files ---", output)
        self.assertIn("/mock/test_dir/config.json", output)
        self.assertIn("/mock/test_dir/notes.md", output)
        self.assertIn("/mock/test_dir/report.txt", output)
        self.assertIn("Total: 3 files found.", output)
        self.assertNotIn("image.jpg", output) # Should not be found

    # Mock rationale: argparse.ArgumentParser.parse_args reads command-line arguments.
    # Mocking it allows us to programmatically provide arguments for testing the main function
    # without actually running the script from the command line.
    # Mock rationale: os.walk interacts with the file system, which is non-deterministic
    # and slow for tests. Mocking it allows us to simulate a consistent file system
    # structure in memory for fast, reliable, and isolated testing.
    @patch('sys.stdout', new_callable=StringIO)
    @patch('os.walk')
    @patch('pathlib.Path.is_dir')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_no_filters_warning(self, mock_parse_args, mock_is_dir, mock_os_walk, mock_stdout):
        mock_is_dir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/test_dir', [], ['file1.txt', 'file2.pdf']),
        ]
        mock_parse_args.return_value = MagicMock(
            path='/mock/test_dir',
            extensions=[],
            keywords=[]
        )

        main()
        output = mock_stdout.getvalue()

        self.assertIn("Warning: No extensions or keywords provided. Listing all files.", output)
        self.assertIn("/mock/test_dir/file1.txt", output)
        self.assertIn("/mock/test_dir/file2.pdf", output)
        self.assertIn("Total: 2 files found.", output)

    # Mock rationale: argparse.ArgumentParser.parse_args reads command-line arguments.
    # Mocking it allows us to programmatically provide arguments for testing the main function
    # without actually running the script from the command line.
    # Mock rationale: os.walk interacts with the file system, which is non-deterministic
    # and slow for tests. Mocking it allows us to simulate a consistent file system
    # structure in memory for fast, reliable, and isolated testing.
    @patch('sys.stdout', new_callable=StringIO)
    @patch('os.walk')
    @patch('pathlib.Path.is_dir')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_no_files_found(self, mock_parse_args, mock_is_dir, mock_os_walk, mock_stdout):
        mock_is_dir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/test_dir', [], ['image.jpg']),
        ]
        mock_parse_args.return_value = MagicMock(
            path='/mock/test_dir',
            extensions=['.txt'],
            keywords=['document']
        )

        main()
        output = mock_stdout.getvalue()

        self.assertIn("No files found matching the criteria.", output)
        self.assertNotIn("image.jpg", output)


if __name__ == '__main__':
    unittest.main()
