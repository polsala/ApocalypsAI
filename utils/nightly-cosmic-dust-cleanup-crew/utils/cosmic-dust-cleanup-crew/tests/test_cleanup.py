import unittest
import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the function to be tested
from src.cleanup import find_cosmic_dust

class TestCosmicDustCleanupCrew(unittest.TestCase):

    def setUp(self):
        """Create a temporary directory structure for testing."""
        self.test_dir = Path("temp_test_repo")
        self.test_dir.mkdir(exist_ok=True)

        # Create some "clean" files
        (self.test_dir / "main.py").touch()
        (self.test_dir / "config.json").touch()
        (self.test_dir / "README.md").touch()

        # Create some "dust" files and directories
        (self.test_dir / "main.py.bak").touch()
        (self.test_dir / "temp_data.csv").touch()
        (self.test_dir / "notes.txt~").touch()
        (self.test_dir / ".DS_Store").touch()
        (self.test_dir / "app.log").touch()
        (self.test_dir / "nested").mkdir()
        (self.test_dir / "nested" / "sub_file.txt.tmp").touch()
        (self.test_dir / "__pycache__").mkdir()
        (self.test_dir / "__pycache__" / "module.cpython-39.pyc").touch()
        (self.test_dir / ".pytest_cache").mkdir()
        (self.test_dir / ".pytest_cache" / "v").mkdir()
        (self.test_dir / ".vscode").mkdir()
        (self.test_dir / ".vscode" / "settings.json").touch()
        (self.test_dir / "my_app.pid").touch()
        (self.test_dir / "db.sqlite3").touch()
        (self.test_dir / ".env.local").touch()
        (self.test_dir / "npm-debug.log").touch()
        (self.test_dir / "file.txt.orig").touch()


    def tearDown(self):
        """Remove the temporary directory after tests."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_find_cosmic_dust_identifies_correct_files(self):
        """
        Test that find_cosmic_dust correctly identifies and returns paths
        for various "dust" files and directories.
        """
        expected_dust = {
            self.test_dir / "main.py.bak",
            self.test_dir / "temp_data.csv",
            self.test_dir / "notes.txt~",
            self.test_dir / ".DS_Store",
            self.test_dir / "app.log",
            self.test_dir / "nested" / "sub_file.txt.tmp",
            self.test_dir / "__pycache__",
            self.test_dir / ".pytest_cache",
            self.test_dir / ".vscode",
            self.test_dir / "my_app.pid",
            self.test_dir / "db.sqlite3",
            self.test_dir / ".env.local",
            self.test_dir / "npm-debug.log",
            self.test_dir / "file.txt.orig",
        }

        found_dust = set(find_cosmic_dust(self.test_dir))

        self.assertEqual(found_dust, expected_dust)
        self.assertNotIn(self.test_dir / "main.py", found_dust)
        self.assertNotIn(self.test_dir / "config.json", found_dust)
        self.assertNotIn(self.test_dir / "README.md", found_dust)
        # Ensure files inside pruned directories are not listed individually
        self.assertNotIn(self.test_dir / "__pycache__" / "module.cpython-39.pyc", found_dust)
        self.assertNotIn(self.test_dir / ".pytest_cache" / "v", found_dust)
        self.assertNotIn(self.test_dir / ".vscode" / "settings.json", found_dust)


    def test_find_cosmic_dust_empty_directory(self):
        """Test with an empty directory."""
        empty_dir = self.test_dir / "empty_folder"
        empty_dir.mkdir()
        self.assertEqual(find_cosmic_dust(empty_dir), [])
        shutil.rmtree(empty_dir)

    def test_find_cosmic_dust_no_dust(self):
        """Test with a directory containing only clean files."""
        clean_dir = self.test_dir / "clean_folder"
        clean_dir.mkdir()
        (clean_dir / "clean_file.txt").touch()
        (clean_dir / "another_clean.py").touch()
        self.assertEqual(find_cosmic_dust(clean_dir), [])
        shutil.rmtree(clean_dir)

    @patch('sys.argv', ['cleanup.py', 'non_existent_path'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_non_existent_path(self, mock_exit, mock_print):
        """
        Test main function behavior when a non-existent path is provided.
        # Mock rationale:
        #   - sys.argv: To simulate command-line arguments without actually running from CLI.
        #   - builtins.print: To capture output for assertion without printing to console during test.
        #   - sys.exit: To prevent the test runner from exiting when the utility calls sys.exit(1).
        """
        from src.cleanup import main # Import here to get the patched sys.argv
        main()
        mock_print.assert_any_call(unittest.mock.ANY, file=unittest.mock.ANY) # Check if print was called for error
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['cleanup.py', 'temp_test_repo/main.py'])
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_path_is_file(self, mock_exit, mock_print):
        """
        Test main function behavior when a file path (not a directory) is provided.
        # Mock rationale:
        #   - sys.argv: To simulate command-line arguments without actually running from CLI.
        #   - builtins.print: To capture output for assertion without printing to console during test.
        #   - sys.exit: To prevent the test runner from exiting when the utility calls sys.exit(1).
        """
        from src.cleanup import main
        main()
        mock_print.assert_any_call(unittest.mock.ANY, file=unittest.mock.ANY)
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['cleanup.py', 'temp_test_repo'])
    @patch('builtins.print')
    def test_main_found_dust_output(self, mock_print):
        """
        Test main function output when dust is found.
        # Mock rationale:
        #   - sys.argv: To simulate command-line arguments without actually running from CLI.
        #   - builtins.print: To capture output for assertion without printing to console during test.
        """
        from src.cleanup import main
        main()
        mock_print.assert_any_call(f"Scanning {self.test_dir.resolve()} for cosmic dust...")
        mock_print.assert_any_call("\nIdentified Cosmic Dust:")
        mock_print.assert_any_call(f"- {self.test_dir.resolve() / 'app.log'}") # Check for one specific dust item
        # We don't assert the exact order of all items, just that the header and some items are present.

    @patch('sys.argv', ['cleanup.py', 'temp_test_repo/clean_folder'])
    @patch('builtins.print')
    def test_main_no_dust_output(self, mock_print):
        """
        Test main function output when no dust is found.
        # Mock rationale:
        #   - sys.argv: To simulate command-line arguments without actually running from CLI.
        #   - builtins.print: To capture output for assertion without printing to console during test.
        """
        from src.cleanup import main
        # Create a clean folder for this specific test
        clean_dir = self.test_dir / "clean_folder"
        clean_dir.mkdir()
        (clean_dir / "clean_file.txt").touch()

        main()
        mock_print.assert_any_call(f"Scanning {clean_dir.resolve()} for cosmic dust...")
        mock_print.assert_any_call("\nNo cosmic dust found. Your repository is sparkling clean!")
        shutil.rmtree(clean_dir)


if __name__ == '__main__':
    unittest.main()
