import unittest
import os
import datetime
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Assume garden_monitor.py is in src/ relative to the test file
# Add the src directory to the path to import garden_monitor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import garden_monitor
sys.path.pop(0) # Clean up path

class TestDigitalGardenMonitor(unittest.TestCase):

    def setUp(self):
        # Define a fixed "current time" for deterministic tests
        self.mock_now = datetime.datetime(2023, 10, 26, 10, 0, 0) # October 26, 2023

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_scan_directory_categorization(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate a valid directory.
        # Mock rationale: os.walk is mocked to simulate a file system structure without actual disk access.
        # Mock rationale: os.path.getmtime is mocked to control file modification times for deterministic age categorization.

        mock_isdir.return_value = True

        # Simulate a directory structure and file modification times
        # File paths are relative to the mocked root for clarity in test setup
        mock_walk.return_value = [
            ('/mock/project', ('sub1', 'sub2'), ('file_blooming.txt', 'file_thriving.py')),
            ('/mock/project/sub1', (), ('file_wilting.md',)),
            ('/mock/project/sub2', (), ('file_fossilized.log', 'another_fossil.bak')),
        ]

        # Define specific modification times relative to self.mock_now
        # Blooming: 2 days ago
        # Thriving: 20 days ago
        # Wilting: 60 days ago
        # Fossilized: 100 days ago, 150 days ago
        mtime_blooming = (self.mock_now - datetime.timedelta(days=2)).timestamp()
        mtime_thriving = (self.mock_now - datetime.timedelta(days=20)).timestamp()
        mtime_wilting = (self.mock_now - datetime.timedelta(days=60)).timestamp()
        mtime_fossilized_1 = (self.mock_now - datetime.timedelta(days=100)).timestamp()
        mtime_fossilized_2 = (self.mock_now - datetime.timedelta(days=150)).timestamp()

        # Map file paths to their mocked mtime
        mtime_map = {
            '/mock/project/file_blooming.txt': mtime_blooming,
            '/mock/project/file_thriving.py': mtime_thriving,
            '/mock/project/sub1/file_wilting.md': mtime_wilting,
            '/mock/project/sub2/file_fossilized.log': mtime_fossilized_1,
            '/mock/project/sub2/another_fossil.bak': mtime_fossilized_2,
        }
        mock_getmtime.side_effect = lambda p: mtime_map[p]

        categorized_files, total_files = garden_monitor.scan_directory('/mock/project', now_dt=self.mock_now)

        self.assertEqual(total_files, 5)
        self.assertIn("Blooming", categorized_files)
        self.assertIn("Thriving", categorized_files)
        self.assertIn("Wilting", categorized_files)
        self.assertIn("Fossilized", categorized_files)

        self.assertEqual(len(categorized_files["Blooming"]), 1)
        self.assertEqual(categorized_files["Blooming"][0][0], '/mock/project/file_blooming.txt')
        self.assertEqual(categorized_files["Blooming"][0][2], 2) # 2 days ago

        self.assertEqual(len(categorized_files["Thriving"]), 1)
        self.assertEqual(categorized_files["Thriving"][0][0], '/mock/project/file_thriving.py')
        self.assertEqual(categorized_files["Thriving"][0][2], 20) # 20 days ago

        self.assertEqual(len(categorized_files["Wilting"]), 1)
        self.assertEqual(categorized_files["Wilting"][0][0], '/mock/project/sub1/file_wilting.md')
        self.assertEqual(categorized_files["Wilting"][0][2], 60) # 60 days ago

        self.assertEqual(len(categorized_files["Fossilized"]), 2)
        fossilized_paths = {f[0] for f in categorized_files["Fossilized"]}
        self.assertIn('/mock/project/sub2/file_fossilized.log', fossilized_paths)
        self.assertIn('/mock/project/sub2/another_fossil.bak', fossilized_paths)
        fossilized_days = {f[2] for f in categorized_files["Fossilized"]}
        self.assertIn(100, fossilized_days)
        self.assertIn(150, fossilized_days)

    @patch('os.path.isdir')
    def test_scan_directory_not_found(self, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate a non-existent directory.
        mock_isdir.return_value = False
        with self.assertRaises(FileNotFoundError):
            garden_monitor.scan_directory('/nonexistent/path', now_dt=self.mock_now)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_scan_directory_empty(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate a valid directory.
        # Mock rationale: os.walk is mocked to simulate an empty file system.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/empty_project', (), ()), # No files
        ]
        mock_getmtime.side_effect = lambda p: (self.mock_now - datetime.timedelta(days=1)).timestamp() # Should not be called

        categorized_files, total_files = garden_monitor.scan_directory('/mock/empty_project', now_dt=self.mock_now)
        self.assertEqual(total_files, 0)
        self.assertEqual(len(categorized_files), 0)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('garden_monitor.scan_directory')
    def test_main_summary_output(self, mock_scan_directory, mock_parse_args, mock_stdout):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control command-line arguments.
        # Mock rationale: garden_monitor.scan_directory is mocked to provide predefined scan results without actual file system interaction.
        # Mock rationale: sys.stdout is mocked to capture printed output for verification.

        mock_parse_args.return_value = MagicMock(path='/mock/project', verbose=False)

        mock_scan_directory.return_value = (
            {
                "Blooming": [('/mock/project/file1.txt', '🌷', 2)],
                "Thriving": [('/mock/project/file2.txt', '🌱', 15)],
                "Wilting": [('/mock/project/file3.txt', '🍂', 45)],
                "Fossilized": [('/mock/project/file4.txt', '💀', 100), ('/mock/project/file5.txt', '💀', 120)],
            },
            5
        )

        garden_monitor.main()

        output = mock_stdout.getvalue()
        self.assertIn("Digital Garden Report for /mock/project:", output)
        self.assertIn("🌷 Blooming (last 7 days): 1 files", output)
        self.assertIn("🌱 Thriving (last 30 days): 1 files", output)
        self.assertIn("🍂 Wilting (last 90 days): 1 files", output)
        self.assertIn("💀 Fossilized (over 90 days): 2 files", output)
        self.assertIn("Total files scanned: 5", output)
        self.assertNotIn("  - ", output) # Ensure verbose output is not present

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('garden_monitor.scan_directory')
    def test_main_verbose_output(self, mock_scan_directory, mock_parse_args, mock_stdout):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control command-line arguments.
        # Mock rationale: garden_monitor.scan_directory is mocked to provide predefined scan results without actual file system interaction.
        # Mock rationale: sys.stdout is mocked to capture printed output for verification.

        mock_parse_args.return_value = MagicMock(path='/mock/project', verbose=True)

        mock_scan_directory.return_value = (
            {
                "Blooming": [('/mock/project/src/main.py', '🌷', 2)],
                "Thriving": [('/mock/project/docs/README.md', '🌱', 15)],
                "Fossilized": [('/mock/project/old/legacy.zip', '💀', 120), ('/mock/project/config/old.ini', '💀', 100)],
            },
            4
        )

        garden_monitor.main()

        output = mock_stdout.getvalue()
        self.assertIn("Digital Garden Report for /mock/project:", output)
        self.assertIn("🌷 Blooming (last 7 days): 1 files", output)
        self.assertIn("  - src/main.py (2 days ago)", output)
        self.assertIn("🌱 Thriving (last 30 days): 1 files", output)
        self.assertIn("  - docs/README.md (15 days ago)", output)
        self.assertIn("💀 Fossilized (over 90 days): 2 files", output)
        # Check for sorted order of fossilized files by days_ago
        self.assertRegex(output, r"  - config/old.ini \(100 days ago\)\n  - old/legacy.zip \(120 days ago\)")
        self.assertIn("Total files scanned: 4", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('garden_monitor.scan_directory')
    @patch('sys.exit')
    def test_main_file_not_found_error(self, mock_exit, mock_scan_directory, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control command-line arguments.
        # Mock rationale: garden_monitor.scan_directory is mocked to simulate a FileNotFoundError.
        # Mock rationale: sys.exit is mocked to prevent actual program exit during testing.
        # Mock rationale: sys.stderr is mocked to capture error output.

        mock_parse_args.return_value = MagicMock(path='/nonexistent/path', verbose=False)
        mock_scan_directory.side_effect = FileNotFoundError("Directory not found: /nonexistent/path")

        garden_monitor.main()

        self.assertIn("Error: Directory not found: /nonexistent/path", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('garden_monitor.scan_directory')
    @patch('sys.exit')
    def test_main_unexpected_error(self, mock_exit, mock_scan_directory, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control command-line arguments.
        # Mock rationale: garden_monitor.scan_directory is mocked to simulate an unexpected error.
        # Mock rationale: sys.exit is mocked to prevent actual program exit during testing.
        # Mock rationale: sys.stderr is mocked to capture error output.

        mock_parse_args.return_value = MagicMock(path='/mock/project', verbose=False)
        mock_scan_directory.side_effect = Exception("Something went wrong!")

        garden_monitor.main()

        self.assertIn("An unexpected error occurred: Something went wrong!", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_get_file_age_category_boundaries(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate a valid directory.
        # Mock rationale: os.walk is mocked to simulate a file system structure.
        # Mock rationale: os.path.getmtime is mocked to control file modification times for deterministic age categorization.

        mock_isdir.return_value = True
        mock_walk.return_value = [('/mock/project', (), ('file.txt',))]

        # Test boundary conditions
        now = self.mock_now

        # Blooming (7 days)
        mtime_7_days_ago = (now - datetime.timedelta(days=7)).timestamp()
        category, emoji, days_ago = garden_monitor.get_file_age_category(mtime_7_days_ago, now)
        self.assertEqual(category, "Blooming")
        self.assertEqual(days_ago, 7)

        # Thriving (8 days ago, just outside blooming)
        mtime_8_days_ago = (now - datetime.timedelta(days=8)).timestamp()
        category, emoji, days_ago = garden_monitor.get_file_age_category(mtime_8_days_ago, now)
        self.assertEqual(category, "Thriving")
        self.assertEqual(days_ago, 8)

        # Thriving (30 days ago)
        mtime_30_days_ago = (now - datetime.timedelta(days=30)).timestamp()
        category, emoji, days_ago = garden_monitor.get_file_age_category(mtime_30_days_ago, now)
        self.assertEqual(category, "Thriving")
        self.assertEqual(days_ago, 30)

        # Wilting (31 days ago, just outside thriving)
        mtime_31_days_ago = (now - datetime.timedelta(days=31)).timestamp()
        category, emoji, days_ago = garden_monitor.get_file_age_category(mtime_31_days_ago, now)
        self.assertEqual(category, "Wilting")
        self.assertEqual(days_ago, 31)

        # Wilting (90 days ago)
        mtime_90_days_ago = (now - datetime.timedelta(days=90)).timestamp()
        category, emoji, days_ago = garden_monitor.get_file_age_category(mtime_90_days_ago, now)
        self.assertEqual(category, "Wilting")
        self.assertEqual(days_ago, 90)

        # Fossilized (91 days ago, just outside wilting)
        mtime_91_days_ago = (now - datetime.timedelta(days=91)).timestamp()
        category, emoji, days_ago = garden_monitor.get_file_age_category(mtime_91_days_ago, now)
        self.assertEqual(category, "Fossilized")
        self.assertEqual(days_ago, 91)

if __name__ == '__main__':
    unittest.main()
