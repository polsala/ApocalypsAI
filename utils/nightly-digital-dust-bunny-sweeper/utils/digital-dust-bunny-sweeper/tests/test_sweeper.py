import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from io import StringIO

# Add the src directory to the path to allow importing sweeper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sweeper import find_dust_bunnies, is_temp_file, report_dust_bunnies, main

class TestSweeper(unittest.TestCase):

    @patch('os.walk')
    @patch('os.path.exists')
    @patch('os.path.join', side_effect=os.path.join) # Mock rationale: os.path.join is deterministic, but patching it ensures consistent path construction in tests.
    def test_find_dust_bunnies_empty_dir(self, mock_join, mock_exists, mock_walk):
        # Mock rationale: Simulate a file system with an empty directory.
        # This allows testing the empty directory detection logic without actual file system interaction.
        mock_exists.return_value = True
        mock_walk.return_value = [
            ('/root', ['empty_dir', 'non_empty_dir'], []), # /root has subdirs
            ('/root/empty_dir', [], []), # This is the empty directory
            ('/root/non_empty_dir', [], ['file.txt']) # This is not empty
        ]
        
        result = find_dust_bunnies(['/root'])
        self.assertIn('/root/empty_dir', result['empty_directories'])
        self.assertNotIn('/root/non_empty_dir', result['empty_directories'])
        self.assertEqual(len(result['empty_directories']), 1)
        self.assertEqual(len(result['temporary_files']), 0)

    @patch('os.walk')
    @patch('os.path.exists')
    @patch('os.path.join', side_effect=os.path.join)
    def test_find_dust_bunnies_temp_files(self, mock_join, mock_exists, mock_walk):
        # Mock rationale: Simulate a file system with various temporary files.
        # This allows testing the temporary file detection logic without actual file system interaction.
        mock_exists.return_value = True
        mock_walk.return_value = [
            ('/root', ['subdir'], ['normal.txt', 'temp.tmp', 'log.log']),
            ('/root/subdir', [], ['~file.txt', 'cache_data.bin', '__pycache__file.pyc'])
        ]
        
        result = find_dust_bunnies(['/root'])
        self.assertIn('/root/temp.tmp', result['temporary_files'])
        self.assertIn('/root/log.log', result['temporary_files'])
        self.assertIn('/root/subdir/~file.txt', result['temporary_files'])
        self.assertIn('/root/subdir/cache_data.bin', result['temporary_files'])
        self.assertIn('/root/subdir/__pycache__file.pyc', result['temporary_files'])
        self.assertNotIn('/root/normal.txt', result['temporary_files'])
        self.assertEqual(len(result['empty_directories']), 0)
        self.assertEqual(len(result['temporary_files']), 5)

    @patch('os.walk')
    @patch('os.path.exists')
    @patch('os.path.join', side_effect=os.path.join)
    def test_find_dust_bunnies_mixed(self, mock_join, mock_exists, mock_walk):
        # Mock rationale: Simulate a complex file system with both empty directories and temporary files.
        # This ensures the utility correctly categorizes both types of dust bunnies.
        mock_exists.return_value = True
        mock_walk.return_value = [
            ('/root', ['empty_dir', 'data_dir'], ['main.py', 'error.log']),
            ('/root/empty_dir', [], []), # Empty directory
            ('/root/data_dir', [], ['report.csv', 'temp_data.tmp', '.DS_Store']) # Contains temp files
        ]
        
        result = find_dust_bunnies(['/root'])
        self.assertIn('/root/empty_dir', result['empty_directories'])
        self.assertIn('/root/error.log', result['temporary_files'])
        self.assertIn('/root/data_dir/temp_data.tmp', result['temporary_files'])
        self.assertIn('/root/data_dir/.DS_Store', result['temporary_files'])
        self.assertEqual(len(result['empty_directories']), 1)
        self.assertEqual(len(result['temporary_files']), 3)

    @patch('os.walk')
    @patch('os.path.exists')
    def test_find_dust_bunnies_non_existent_path(self, mock_exists, mock_walk):
        # Mock rationale: Test how the utility handles a path that does not exist.
        # This ensures graceful handling and error reporting without crashing.
        mock_exists.return_value = False
        
        # Capture stdout to check the warning message
        captured_output = StringIO()
        sys.stdout = captured_output
        
        result = find_dust_bunnies(['/non/existent/path'])
        
        sys.stdout = sys.__stdout__ # Restore stdout
        self.assertIn("Warning: Path '/non/existent/path' does not exist. Skipping.", captured_output.getvalue())
        self.assertEqual(len(result['empty_directories']), 0)
        self.assertEqual(len(result['temporary_files']), 0)
        mock_walk.assert_not_called() # os.walk should not be called if path doesn't exist

    def test_is_temp_file(self):
        # Mock rationale: Directly test the helper function with various inputs.
        # This verifies the pattern matching logic for temporary files in isolation.
        self.assertTrue(is_temp_file("report.tmp"))
        self.assertTrue(is_temp_file("application.log"))
        self.assertTrue(is_temp_file("~document.docx"))
        self.assertTrue(is_temp_file("file.bak"))
        self.assertTrue(is_temp_file(".DS_Store"))
        self.assertTrue(is_temp_file("cache_file.txt"))
        self.assertTrue(is_temp_file("temp_report.pdf"))
        self.assertTrue(is_temp_file("__pycache__file.pyc")) 
        self.assertTrue(is_temp_file("npm-debug.log"))
        self.assertTrue(is_temp_file("error.log"))
        self.assertFalse(is_temp_file("important.txt"))
        self.assertFalse(is_temp_file("image.jpg"))
        self.assertFalse(is_temp_file("document.pdf"))

    def test_report_dust_bunnies_no_bunnies(self):
        # Mock rationale: Test the reporting function when no dust bunnies are found.
        # This ensures the correct "clean" message is displayed.
        dust_bunnies = {"empty_directories": [], "temporary_files": []}
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        report_dust_bunnies(dust_bunnies)
        
        sys.stdout = sys.__stdout__
        self.assertIn("Your digital space is sparkling clean! No dust bunnies found.", captured_output.getvalue())

    def test_report_dust_bunnies_with_bunnies(self):
        # Mock rationale: Test the reporting function when dust bunnies are found.
        # This verifies the formatted output and summary are correct.
        dust_bunnies = {
            "empty_directories": ["/root/empty_dir"],
            "temporary_files": ["/root/log.log", "/root/temp.tmp"] # Sorted for deterministic test
        }
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        report_dust_bunnies(dust_bunnies)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Oh dear! It looks like we've found some digital dust bunnies", output)
        self.assertIn("👻 Empty Directories (Ghostly Hollows):", output)
        self.assertIn("  - /root/empty_dir", output)
        self.assertIn("(1 empty directories found)", output)
        self.assertIn("🗑️ Temporary Files (Ephemeral Clutter):", output)
        self.assertIn("  - /root/log.log", output)
        self.assertIn("  - /root/temp.tmp", output)
        self.assertIn("(2 temporary files found)", output)
        self.assertIn("Total Digital Dust Bunnies Spotted: 3", output)
        self.assertIn("Recommendation: Consider tidying up these paths.", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.find_dust_bunnies')
    @patch('sweeper.report_dust_bunnies')
    @patch('os.path.exists') # Mock rationale: Ensure os.path.exists is mocked for main function's internal calls.
    def test_main_function(self, mock_exists, mock_report, mock_find, mock_parse_args):
        # Mock rationale: Test the main CLI entry point.
        # This ensures argument parsing and the orchestration of core functions work as expected.
        mock_parse_args.return_value = MagicMock(path=['/test/path'])
        mock_find.return_value = {"empty_directories": [], "temporary_files": []}
        mock_exists.return_value = True # Ensure find_dust_bunnies doesn't skip the path

        # Capture stdout to check initial print statement
        captured_output = StringIO()
        sys.stdout = captured_output

        main()

        sys.stdout = sys.__stdout__
        self.assertIn("Scanning 1 path(s) for digital dust bunnies...", captured_output.getvalue())
        mock_find.assert_called_once_with(['/test/path'])
        mock_report.assert_called_once_with({"empty_directories": [], "temporary_files": []})

if __name__ == '__main__':
    unittest.main()
