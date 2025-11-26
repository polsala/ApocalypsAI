import unittest
import tempfile
import shutil
import os
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

# Import the function to be tested
from src.checker import check_survival_kit, main, DEFAULT_ESSENTIAL_FILES

class TestSurvivalKitChecker(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = Path(tempfile.mkdtemp())
        # Redirect stdout and stderr to capture print statements
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self.captured_output = StringIO()
        sys.stdout = self.captured_output
        sys.stderr = self.captured_output

    def tearDown(self):
        # Clean up the temporary directory and restore stdout/stderr
        shutil.rmtree(self.test_dir)
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

    def _create_file(self, relative_path: str):
        """Helper to create a file within the test directory."""
        file_path = self.test_dir / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()

    def _create_dir(self, relative_path: str):
        """Helper to create a directory within the test directory."""
        dir_path = self.test_dir / relative_path
        dir_path.mkdir(parents=True, exist_ok=True)

    def test_all_essential_files_present(self):
        # Mock rationale: Creating actual files/directories in a temporary directory is deterministic
        # and offline, accurately simulating the file system state without external dependencies.
        self._create_file("README.md")
        self._create_file("LICENSE")
        self._create_file(".gitignore")
        self._create_file("requirements.txt")
        self._create_file(".env")

        results = check_survival_kit(self.test_dir, DEFAULT_ESSENTIAL_FILES)
        self.assertTrue(all(results.values()), "All essential files should be present.")
        self.assertEqual(len(results), len(DEFAULT_ESSENTIAL_FILES))

    def test_some_essential_files_missing(self):
        # Mock rationale: Creating actual files/directories in a temporary directory is deterministic
        # and offline, accurately simulating the file system state without external dependencies.
        self._create_file("README.md")
        self._create_file("LICENSE")
        # .gitignore, requirements.txt, .env are missing

        results = check_survival_kit(self.test_dir, DEFAULT_ESSENTIAL_FILES)
        self.assertFalse(results[".gitignore"], ".gitignore should be missing.")
        self.assertFalse(results["requirements.txt"], "requirements.txt should be missing.")
        self.assertFalse(results[".env"], ".env should be missing.")
        self.assertTrue(results["README.md"], "README.md should be present.")
        self.assertTrue(results["LICENSE"], "LICENSE should be present.")
        self.assertEqual(len(results), len(DEFAULT_ESSENTIAL_FILES))

    def test_custom_essential_items(self):
        # Mock rationale: Creating actual files/directories in a temporary directory is deterministic
        # and offline, accurately simulating the file system state without external dependencies.
        custom_items = ["config.json", "data/", "main.py"]
        self._create_file("config.json")
        self._create_dir("data/")

        results = check_survival_kit(self.test_dir, custom_items)
        self.assertTrue(results["config.json"], "config.json should be present.")
        self.assertTrue(results["data/"], "data/ directory should be present.")
        self.assertFalse(results["main.py"], "main.py should be missing.")
        self.assertEqual(len(results), len(custom_items))

    def test_empty_directory(self):
        # Mock rationale: Using an empty temporary directory directly tests the scenario.
        results = check_survival_kit(self.test_dir, DEFAULT_ESSENTIAL_FILES)
        self.assertTrue(all(not v for v in results.values()), "No items should be present in an empty directory.")

    @patch('sys.exit')
    def test_main_function_success(self, mock_exit):
        # Mock rationale: patch sys.argv to simulate command-line arguments and
        # patch sys.exit to prevent actual program termination during test. Output is
        # captured via StringIO for assertion, ensuring deterministic and offline testing.
        self._create_file("README.md")
        self._create_file("LICENSE")

        with patch('sys.argv', ['src/checker.py', '--path', str(self.test_dir), '--files', 'README.md,LICENSE']):
            main()
            mock_exit.assert_not_called() # Should not exit with error
            output = self.captured_output.getvalue()
            self.assertIn("🎉 All 2 essential items found! Your project is apocalypse-ready!", output)

    @patch('sys.exit')
    def test_main_function_missing_files_exit_1(self, mock_exit):
        # Mock rationale: patch sys.argv to simulate command-line arguments and
        # patch sys.exit to prevent actual program termination during test. Output is
        # captured via StringIO for assertion, ensuring deterministic and offline testing.
        self._create_file("README.md") # Only README.md is present

        with patch('sys.argv', ['src/checker.py', '--path', str(self.test_dir), '--files', 'README.md,LICENSE']):
            main()
            mock_exit.assert_called_once_with(1) # Should exit with error code 1
            output = self.captured_output.getvalue()
            self.assertIn("⚠️  1 essential items MISSING. 1 found. Prepare for potential fallout!", output)

    @patch('sys.exit')
    def test_main_function_invalid_path_exit_1(self, mock_exit):
        # Mock rationale: patch sys.argv to simulate command-line arguments and
        # patch sys.exit to prevent actual program termination during test. Output is
        # captured via StringIO for assertion, ensuring deterministic and offline testing.
        invalid_path = self.test_dir / "non_existent_dir"

        with patch('sys.argv', ['src/checker.py', '--path', str(invalid_path), '--files', 'README.md']):
            main()
            mock_exit.assert_called_once_with(1) # Should exit with error code 1
            output = self.captured_output.getvalue()
            self.assertIn(f"🚨 ERROR: Project path '{invalid_path}' is not a valid directory. Aborting survival check!", output)

    @patch('sys.exit')
    def test_main_function_no_files_specified_exit_0(self, mock_exit):
        # Mock rationale: patch sys.argv to simulate command-line arguments and
        # patch sys.exit to prevent actual program termination during test. Output is
        # captured via StringIO for assertion, ensuring deterministic and offline testing.
        with patch('sys.argv', ['src/checker.py', '--path', str(self.test_dir), '--files', '']):
            main()
            mock_exit.assert_called_once_with(0) # Should exit with 0 (no-op)
            output = self.captured_output.getvalue()
            self.assertIn("⚠️ WARNING: No essential files/directories specified. Nothing to check!", output)
