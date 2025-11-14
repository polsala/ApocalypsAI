import unittest
from unittest.mock import patch, MagicMock
import os
import time
from datetime import datetime, timedelta

# Import the function to be tested
from src.dust_bunny_sweeper import find_dust_bunnies, main

class TestDustBunnySweeper(unittest.TestCase):

    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    @patch('os.path.abspath')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_find_dust_bunnies_and_main_integration(self, mock_stdout, mock_parse_args, mock_abspath, mock_getmtime, mock_isdir, mock_walk):
        # Mock rationale: Simulate command-line arguments for main()
        mock_parse_args.return_value = MagicMock(
            path="/mock/project",
            age=365,
            patterns=None
        )
        # Mock rationale: Ensure abspath returns the mocked path
        mock_abspath.return_value = "/mock/project"
        # Mock rationale: Simulate the target path as a valid directory
        mock_isdir.side_effect = lambda p: p == "/mock/project"

        # Mock rationale: Simulate current time for age calculation
        mock_now = time.time()
        one_year_ago = mock_now - (365 * 24 * 60 * 60)
        six_months_ago = mock_now - (180 * 24 * 60 * 60)

        # Mock rationale: Simulate file system structure and modification times
        mock_walk.return_value = [
            ("/mock/project", ["empty_dir", "src", "build", "node_modules"], ["README.md", "old_file.log"]),
            ("/mock/project/empty_dir", [], []), # An empty directory
            ("/mock/project/src", [], ["app.py", "temp.tmp", "__pycache__.pyc"]),
            ("/mock/project/build", [], ["output.exe"]), # A pattern-matched file
            ("/mock/project/node_modules", [], ["package.json"]) # A pattern-matched directory
        ]

        # Mock rationale: Provide specific modification times for files
        def mock_getmtime_side_effect(path):
            if path == "/mock/project/README.md":
                return six_months_ago # Not ancient
            elif path == "/mock/project/old_file.log":
                return one_year_ago - 100 # Definitely ancient
            elif path == "/mock/project/src/app.py":
                return mock_now # Not ancient
            elif path == "/mock/project/src/temp.tmp":
                return mock_now # Pattern-matched, but not ancient
            elif path == "/mock/project/src/__pycache__.pyc":
                return mock_now # Pattern-matched, but not ancient
            elif path == "/mock/project/build/output.exe":
                return mock_now # Pattern-matched, but not ancient
            elif path == "/mock/project/node_modules/package.json":
                return mock_now # Inside pattern-matched dir, but not directly checked
            return mock_now # Default for other files

        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Run the main function
        main()

        # Assertions for the report output
        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)

        self.assertIn("Scanning /mock/project for digital dust bunnies...", output_str)
        self.assertIn("--- Digital Dust Bunny Report ---", output_str)

        # Check for empty directories
        self.assertIn("🧹 Empty Directories:", output_str)
        self.assertIn("  - /mock/project/empty_dir", output_str)

        # Check for ancient files
        self.assertIn("⏳ Ancient Files (older than 365 days):", output_str)
        self.assertIn(f"  - /mock/project/old_file.log (Last modified: {datetime.fromtimestamp(one_year_ago - 100).strftime('%Y-%m-%d')})", output_str)
        self.assertNotIn("/mock/project/README.md", output_str) # Should not be ancient

        # Check for pattern-matched files/directories
        self.assertIn("🗑️ Temporary/Pattern-Matched Files & Directories:", output_str)
        self.assertIn("  - /mock/project/src/temp.tmp", output_str)
        self.assertIn("  - /mock/project/src/__pycache__.pyc", output_str)
        self.assertIn("  - /mock/project/build/output.exe", output_str)
        self.assertIn("  - /mock/project/node_modules", output_str) # The directory itself should be flagged

        # Check total count
        self.assertIn("Found 5 digital dust bunnies. Time for a cleanup!", output_str)

    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_no_bunnies(self, mock_getmtime, mock_isdir, mock_walk):
        # Mock rationale: Simulate a clean project with no dust bunnies
        mock_walk.return_value = [
            ("/mock/clean_project", ["src"], ["main.py", "config.ini"]),
            ("/mock/clean_project/src", [], ["module.py"])
        ]
        # Mock rationale: All files are recent
        mock_getmtime.return_value = time.time()
        # Mock rationale: All paths are directories
        mock_isdir.return_value = True

        dust_bunnies = find_dust_bunnies("/mock/clean_project", min_age_days=365)

        self.assertEqual(len(dust_bunnies["empty_dirs"]), 0)
        self.assertEqual(len(dust_bunnies["ancient_files"]), 0)
        self.assertEqual(len(dust_bunnies["pattern_files"]), 0)

    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_with_extra_patterns(self, mock_getmtime, mock_isdir, mock_walk):
        # Mock rationale: Simulate a project with custom pattern files
        mock_walk.return_value = [
            ("/mock/project", [], ["data.csv", "backup.bak", "temp_report.log"])
        ]
        # Mock rationale: All files are recent, so only patterns should match
        mock_getmtime.return_value = time.time()
        # Mock rationale: All paths are directories
        mock_isdir.return_value = True

        extra_patterns = ["*.bak", "*.csv"]
        dust_bunnies = find_dust_bunnies("/mock/project", min_age_days=365, extra_patterns=extra_patterns)

        self.assertEqual(len(dust_bunnies["empty_dirs"]), 0)
        self.assertEqual(len(dust_bunnies["ancient_files"]), 0)
        self.assertEqual(len(dust_bunnies["pattern_files"]), 3) # .bak, .csv, and .log (default)

        self.assertIn("/mock/project/backup.bak", dust_bunnies["pattern_files"])
        self.assertIn("/mock/project/data.csv", dust_bunnies["pattern_files"])
        self.assertIn("/mock/project/temp_report.log", dust_bunnies["pattern_files"]) # Default pattern

    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_directory_pattern_matching(self, mock_getmtime, mock_isdir, mock_walk):
        # Mock rationale: Simulate a project with a 'node_modules' directory
        mock_walk.return_value = [
            ("/mock/project", ["node_modules", "src"], ["main.py"]),
            ("/mock/project/node_modules", ["some_lib"], ["package.json"]), # Should not be walked into
            ("/mock/project/node_modules/some_lib", [], ["index.js"]),
            ("/mock/project/src", [], ["util.py"])
        ]
        mock_getmtime.return_value = time.time()
        mock_isdir.return_value = True # Assume all paths are directories for simplicity in this test

        dust_bunnies = find_dust_bunnies("/mock/project", min_age_days=365)

        self.assertIn("/mock/project/node_modules", dust_bunnies["pattern_files"])
        # Ensure that 'node_modules' sub-contents are NOT listed as separate pattern files
        # because the parent directory was matched and recursion stopped.
        self.assertNotIn("/mock/project/node_modules/package.json", dust_bunnies["pattern_files"])
        self.assertNotIn("/mock/project/node_modules/some_lib", dust_bunnies["pattern_files"])
        self.assertNotIn("/mock/project/node_modules/some_lib/index.js", dust_bunnies["pattern_files"])

        # Ensure other files are not affected
        self.assertNotIn("/mock/project/main.py", dust_bunnies["pattern_files"])
        self.assertNotIn("/mock/project/src/util.py", dust_bunnies["pattern_files"])


    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_os_error_on_getmtime(self, mock_getmtime, mock_isdir, mock_walk):
        # Mock rationale: Simulate a file being deleted between os.walk and os.path.getmtime
        mock_walk.return_value = [
            ("/mock/project", [], ["existing_file.txt", "deleted_file.txt"])
        ]
        mock_isdir.return_value = True

        def getmtime_side_effect(path):
            if "deleted_file.txt" in path:
                raise OSError("File not found")
            return time.time() - (366 * 24 * 60 * 60) # Make existing_file ancient

        mock_getmtime.side_effect = getmtime_side_effect

        dust_bunnies = find_dust_bunnies("/mock/project", min_age_days=365)

        self.assertEqual(len(dust_bunnies["ancient_files"]), 1)
        self.assertIn("/mock/project/existing_file.txt", [f[0] for f in dust_bunnies["ancient_files"]])
        self.assertNotIn("/mock/project/deleted_file.txt", [f[0] for f in dust_bunnies["ancient_files"]])
        self.assertEqual(len(dust_bunnies["empty_dirs"]), 0)
        self.assertEqual(len(dust_bunnies["pattern_files"]), 0)


if __name__ == '__main__':
    unittest.main()
