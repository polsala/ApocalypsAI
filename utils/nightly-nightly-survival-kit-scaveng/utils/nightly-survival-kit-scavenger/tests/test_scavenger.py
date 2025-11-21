import unittest
import os
import sys
from unittest.mock import patch, mock_open
from io import StringIO

# Adjust path to import scavenger.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from scavenger import check_project_survival_kit, ESSENTIAL_FILES, ESSENTIAL_DIRS

class TestSurvivalKitScavenger(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open) # Mock open for pyproject.toml content
    def test_all_files_present(self, mock_file_open, mock_exists, mock_isdir):
        # Mock rationale: Simulate a directory where all essential files and dirs exist.
        # This allows testing the 'all present' scenario without actual file system interaction.
        mock_isdir.side_effect = lambda p: p == "/mock/project" or p == "/mock/project/docs"
        mock_exists.side_effect = lambda p: (
            p == "/mock/project/README.md" or
            p == "/mock/project/LICENSE" or
            p == "/mock/project/requirements.txt" or
            p == "/mock/project/Dockerfile" or
            p == "/mock/project/Makefile" or
            p == "/mock/project/.gitignore" or
            p == "/mock/project/pyproject.toml" or
            p == "/mock/project/CONTRIBUTING.md"
        )
        mock_file_open.return_value.read.return_value = "" # pyproject.toml not relevant here for this test

        missing, present = check_project_survival_kit("/mock/project")

        self.assertEqual(len(missing), 0)
        self.assertEqual(len(present), len(ESSENTIAL_FILES) + len(ESSENTIAL_DIRS))
        output = self.captured_output.getvalue()
        self.assertIn("Your project's survival kit is complete!", output)
        for item in ESSENTIAL_FILES:
            self.assertIn(f"✅ {item}", output)
        for item in ESSENTIAL_DIRS:
            self.assertIn(f"✅ {item}/", output)

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_some_files_missing(self, mock_file_open, mock_exists, mock_isdir):
        # Mock rationale: Simulate a directory where some essential files are missing.
        # This tests the reporting of missing items.
        mock_isdir.side_effect = lambda p: p == "/mock/project" or p == "/mock/project/docs"
        mock_exists.side_effect = lambda p: (
            p == "/mock/project/README.md" or
            p == "/mock/project/LICENSE" or
            p == "/mock/project/.gitignore" or
            p == "/mock/project/pyproject.toml" # pyproject.toml exists, but no requirements.txt
        )
        mock_file_open.return_value.read.return_value = "" # pyproject.toml exists but no relevant content

        missing, present = check_project_survival_kit("/mock/project")

        expected_missing = [
            "requirements.txt", "Dockerfile", "Makefile", "CONTRIBUTING.md"
        ]
        self.assertCountEqual(missing, expected_missing)
        self.assertEqual(len(present), len(ESSENTIAL_FILES) + len(ESSENTIAL_DIRS) - len(expected_missing))
        output = self.captured_output.getvalue()
        self.assertIn("Your project is missing 4 essential survival items.", output)
        self.assertIn("Consider adding: requirements.txt, Dockerfile, Makefile, CONTRIBUTING.md", output)
        self.assertIn("❌ requirements.txt", output)
        self.assertIn("✅ README.md", output)
        self.assertIn("✅ docs/", output) # docs dir is present

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_empty_directory(self, mock_file_open, mock_exists, mock_isdir):
        # Mock rationale: Simulate an empty directory.
        # This tests the scenario where almost everything is missing.
        mock_isdir.side_effect = lambda p: p == "/mock/empty-project"
        mock_exists.return_value = False
        mock_file_open.return_value.read.return_value = ""

        missing, present = check_project_survival_kit("/mock/empty-project")

        self.assertEqual(len(missing), len(ESSENTIAL_FILES) + len(ESSENTIAL_DIRS))
        self.assertEqual(len(present), 0)
        output = self.captured_output.getvalue()
        self.assertIn(f"Your project is missing {len(ESSENTIAL_FILES) + len(ESSENTIAL_DIRS)} essential survival items.", output)
        self.assertIn("❌ README.md", output)
        self.assertIn("❌ docs/", output)

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_invalid_path(self, mock_file_open, mock_exists, mock_isdir):
        # Mock rationale: Simulate an invalid project path (not a directory).
        # This tests the error handling for invalid input.
        mock_isdir.return_value = False
        mock_exists.return_value = False # Not strictly needed for this test, but good practice

        with self.assertRaises(SystemExit) as cm:
            check_project_survival_kit("/invalid/path")
        self.assertEqual(cm.exception.code, 1)
        output = self.captured_output.getvalue()
        self.assertIn("Error: Project path '/invalid/path' is not a valid directory.", output)

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_pyproject_toml_covers_requirements(self, mock_file_open, mock_exists, mock_isdir):
        # Mock rationale: Simulate a project with pyproject.toml containing poetry/project section,
        # but no requirements.txt. This tests the special logic for Python dependency files.
        mock_isdir.side_effect = lambda p: p == "/mock/project" or p == "/mock/project/docs"
        mock_exists.side_effect = lambda p: (
            p == "/mock/project/README.md" or
            p == "/mock/project/LICENSE" or
            p == "/mock/project/Dockerfile" or
            p == "/mock/project/.gitignore" or
            p == "/mock/project/pyproject.toml" or # pyproject.toml exists
            p == "/mock/project/CONTRIBUTING.md"
        )
        # Mock pyproject.toml content to indicate it handles dependencies
        mock_file_open.return_value.read.return_value = "[tool.poetry]\nname = \"my-project\""

        missing, present = check_project_survival_kit("/mock/project")

        # requirements.txt should NOT be in missing, as pyproject.toml covers it
        self.assertNotIn("requirements.txt", missing)
        self.assertIn("requirements.txt", present) # It's considered 'present' via pyproject.toml
        output = self.captured_output.getvalue()
        self.assertIn("✅ requirements.txt (Python dependency rations - via pyproject.toml)", output)
        self.assertNotIn("❌ requirements.txt", output)

        # Ensure other missing files are still reported
        expected_missing = ["Makefile"]
        self.assertCountEqual(missing, expected_missing)
        self.assertIn("Your project is missing 1 essential survival item.", output)
        self.assertIn("Consider adding: Makefile", output)

    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_pyproject_toml_without_dependency_section(self, mock_file_open, mock_exists, mock_isdir):
        # Mock rationale: Simulate a project with pyproject.toml but without poetry/project section,
        # and no requirements.txt. This tests that requirements.txt is still marked missing.
        mock_isdir.side_effect = lambda p: p == "/mock/project" or p == "/mock/project/docs"
        mock_exists.side_effect = lambda p: (
            p == "/mock/project/README.md" or
            p == "/mock/project/LICENSE" or
            p == "/mock/project/Dockerfile" or
            p == "/mock/project/.gitignore" or
            p == "/mock/project/pyproject.toml" or # pyproject.toml exists
            p == "/mock/project/CONTRIBUTING.md"
        )
        # Mock pyproject.toml content without relevant sections
        mock_file_open.return_value.read.return_value = "[tool.black]\nline-length = 88"

        missing, present = check_project_survival_kit("/mock/project")

        # requirements.txt should be in missing
        self.assertIn("requirements.txt", missing)
        self.assertNotIn("requirements.txt", present)
        output = self.captured_output.getvalue()
        self.assertIn("❌ requirements.txt", output)

        expected_missing = ["requirements.txt", "Makefile"]
        self.assertCountEqual(missing, expected_missing)
        self.assertIn("Your project is missing 2 essential survival items.", output)
        self.assertIn("Consider adding: requirements.txt, Makefile", output)


if __name__ == '__main__':
    unittest.main()
