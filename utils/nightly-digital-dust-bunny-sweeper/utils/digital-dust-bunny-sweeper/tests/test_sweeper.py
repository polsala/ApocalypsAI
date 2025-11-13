import unittest
import os
import tempfile
import shutil
from unittest.mock import patch
import sys

# Mock rationale: We need to import the function directly to test it in isolation
# without relying on the script's main execution path for unit tests.
from src.sweeper import find_dust_bunnies, main

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Create a temporary directory structure for each test.
        # This ensures tests are isolated, deterministic, and don't affect the actual filesystem.
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Mock rationale: Clean up the temporary directory after each test.
        # This ensures no test artifacts are left behind.
        shutil.rmtree(self.test_dir)

    def _create_file(self, path, content=""): # Helper to create files
        full_path = os.path.join(self.test_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)

    def _create_dir(self, path): # Helper to create directories
        full_path = os.path.join(self.test_dir, path)
        os.makedirs(full_path, exist_ok=True)

    def test_find_empty_directories(self):
        self._create_dir("empty_dir_1")
        self._create_dir("parent/empty_dir_2")
        self._create_file("parent/not_empty/file.txt")

        empty_dirs, junk_files = find_dust_bunnies(self.test_dir)

        expected_empty_dirs = [
            "empty_dir_1",
            os.path.join("parent", "empty_dir_2")
        ]
        self.assertCountEqual(empty_dirs, expected_empty_dirs)
        self.assertEqual(junk_files, [])

    def test_find_junk_files(self):
        self._create_file("app.log")
        self._create_file("temp/data.tmp")
        self._create_file("build/output.bak")
        self._create_file("src/module.pyc")
        self._create_file("src/__pycache__/module.cpython-39.pyc")
        self._create_file(".DS_Store")
        self._create_file("Thumbs.db")
        self._create_file("normal_file.txt") # Should not be detected

        empty_dirs, junk_files = find_dust_bunnies(self.test_dir)

        expected_junk_files = [
            "app.log",
            os.path.join("temp", "data.tmp"),
            os.path.join("build", "output.bak"),
            "src/module.pyc",
            ".DS_Store",
            "Thumbs.db",
            os.path.join("src", "__pycache__") # __pycache__ is a junk dir, so its contents are filtered out
        ]
        self.assertCountEqual(junk_files, expected_junk_files)
        self.assertEqual(empty_dirs, [])

    def test_find_junk_directories(self):
        self._create_dir("node_modules/some_package")
        self._create_file("node_modules/some_package/index.js")
        self._create_dir("dist/assets")
        self._create_file("dist/assets/image.png")
        self._create_dir("build/temp")
        self._create_file("build/temp/file.txt")
        self._create_dir("venv/bin")
        self._create_file("venv/bin/python")
        self._create_dir(".pytest_cache")
        self._create_file(".pytest_cache/some_file")
        self._create_dir(".mypy_cache")
        self._create_file(".mypy_cache/some_file")
        self._create_file("src/main.py")

        empty_dirs, junk_files = find_dust_bunnies(self.test_dir)

        expected_junk_items = [
            "node_modules",
            "dist",
            "build",
            "venv",
            ".pytest_cache",
            ".mypy_cache"
        ]
        # The sweeper should list the top-level junk directories, not their contents
        self.assertCountEqual(junk_files, expected_junk_items)
        self.assertEqual(empty_dirs, [])

    def test_mixed_scenario(self):
        self._create_dir("empty_dir")
        self._create_file("logs/debug.log")
        self._create_file("src/main.py")
        self._create_dir("node_modules/package")
        self._create_file("node_modules/package/file.js")
        self._create_file("temp.tmp")
        self._create_dir("another_empty")
        self._create_file("src/__pycache__/module.cpython-39.pyc")

        empty_dirs, junk_files = find_dust_bunnies(self.test_dir)

        expected_empty_dirs = [
            "empty_dir",
            "another_empty"
        ]
        expected_junk_files = [
            os.path.join("logs", "debug.log"),
            "node_modules", # Should list the directory, not its contents
            "temp.tmp",
            os.path.join("src", "__pycache__") # Should list the __pycache__ dir, not the .pyc file inside
        ]

        self.assertCountEqual(empty_dirs, expected_empty_dirs)
        self.assertCountEqual(junk_files, expected_junk_files)

    def test_main_script_output(self):
        self._create_dir("empty_dir")
        self._create_file("test.log")
        self._create_file("src/main.py")

        # Mock rationale: Capture stdout to verify the script's printed output.
        # This allows testing the main function's user-facing behavior without actual console interaction.
        with patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout,
             patch('sys.argv', ['sweeper.py', self.test_dir]),
             patch('sys.exit') as mock_exit:
            main()

            output = mock_stdout.getvalue()
            self.assertIn("Digital Dust Bunny Sweeper Report:", output)
            self.assertIn("Empty Directories:", output)
            self.assertIn("- empty_dir", output)
            self.assertIn("Junk Files/Directories:", output)
            self.assertIn("- test.log", output)
            mock_exit.assert_called_once_with(0)

    def test_main_script_no_bunnies(self):
        self._create_file("src/main.py")
        self._create_file("README.md")

        with patch('sys.stdout', new_callable=unittest.mock.StringIO) as mock_stdout,
             patch('sys.argv', ['sweeper.py', self.test_dir]),
             patch('sys.exit') as mock_exit:
            main()

            output = mock_stdout.getvalue()
            self.assertIn(f"No digital dust bunnies found in '{self.test_dir}'. Your project is sparkling clean! ✨", output)
            mock_exit.assert_called_once_with(0)

    def test_main_script_invalid_path(self):
        invalid_path = os.path.join(self.test_dir, "non_existent_dir")

        with patch('sys.stderr', new_callable=unittest.mock.StringIO) as mock_stderr,
             patch('sys.argv', ['sweeper.py', invalid_path]),
             patch('sys.exit') as mock_exit:
            main()

            output = mock_stderr.getvalue()
            self.assertIn(f"Error: '{invalid_path}' is not a valid directory.", output)
            mock_exit.assert_called_once_with(1)
