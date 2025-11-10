import unittest
import os
import tempfile
import zipfile
import datetime
from unittest import mock

# Adjust the import path for testing when running from the tests/ directory
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from ark_builder import build_ark, main

class TestArkBuilder(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Using TemporaryDirectory ensures tests are isolated,
        # deterministic, and don't interfere with the actual filesystem.
        # It simulates a real filesystem environment for robust testing of file operations.
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = self.temp_dir.name

        self.output_zip_path = os.path.join(self.base_path, "test_ark.zip")

    def tearDown(self):
        # Clean up the temporary directory and its contents
        self.temp_dir.cleanup()

    def _create_dummy_file(self, path, content="dummy content"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return path

    def _get_zip_contents(self, zip_path):
        """Helper to get a list of file names inside a zip archive."""
        with zipfile.ZipFile(zip_path, 'r') as zf:
            return zf.namelist()

    def _get_zip_file_content(self, zip_path, filename):
        """Helper to get content of a specific file inside a zip archive."""
        with zipfile.ZipFile(zip_path, 'r') as zf:
            with zf.open(filename) as f:
                return f.read().decode('utf-8')

    def test_build_ark_single_file(self):
        file_path = self._create_dummy_file(os.path.join(self.base_path, "document.txt"))
        
        # Mock rationale: datetime.datetime.now() is non-deterministic.
        # Mocking it ensures the manifest content is predictable for testing.
        mock_now = datetime.datetime(2023, 1, 1, 12, 0, 0)
        with mock.patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = mock_now
            mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw) # Allow other datetime calls
            archived_items = build_ark([file_path], self.output_zip_path)

        self.assertTrue(os.path.exists(self.output_zip_path))
        
        expected_contents = ['document.txt', 'MANIFEST.txt']
        self.assertCountEqual(expected_contents, self._get_zip_contents(self.output_zip_path))

        manifest_content = self._get_zip_file_content(self.output_zip_path, 'MANIFEST.txt')
        self.assertIn("ApocalypsAI Data Ark Manifest", manifest_content)
        self.assertIn(f"Created: {mock_now.isoformat()}", manifest_content)
        self.assertIn(f"Source Paths: {file_path}", manifest_content)
        self.assertIn("- document.txt", manifest_content)
        self.assertEqual(len(archived_items), len(expected_contents))

    def test_build_ark_directory(self):
        dir_path = os.path.join(self.base_path, "my_data")
        self._create_dummy_file(os.path.join(dir_path, "docs", "report.txt"))
        self._create_dummy_file(os.path.join(dir_path, "images", "photo.jpg"))
        self._create_dummy_file(os.path.join(dir_path, "notes.md"))

        mock_now = datetime.datetime(2023, 1, 1, 12, 0, 0)
        with mock.patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = mock_now
            mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
            archived_items = build_ark([dir_path], self.output_zip_path)

        self.assertTrue(os.path.exists(self.output_zip_path))

        # Expected paths inside the zip, relative to the base of the source directory
        expected_contents = [
            'my_data/docs/report.txt',
            'my_data/images/photo.jpg',
            'my_data/notes.md',
            'MANIFEST.txt'
        ]
        self.assertCountEqual(expected_contents, self._get_zip_contents(self.output_zip_path))

        manifest_content = self._get_zip_file_content(self.output_zip_path, 'MANIFEST.txt')
        self.assertIn("- my_data/docs/report.txt", manifest_content)
        self.assertIn("- my_data/images/photo.jpg", manifest_content)
        self.assertIn("- my_data/notes.md", manifest_content)
        self.assertEqual(len(archived_items), len(expected_contents))

    def test_build_ark_multiple_sources(self):
        file_path = self._create_dummy_file(os.path.join(self.base_path, "important.txt"))
        dir_path = os.path.join(self.base_path, "secret_plans")
        self._create_dummy_file(os.path.join(dir_path, "phase1.doc"))
        self._create_dummy_file(os.path.join(dir_path, "phase2.doc"))

        mock_now = datetime.datetime(2023, 1, 1, 12, 0, 0)
        with mock.patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value = mock_now
            mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
            archived_items = build_ark([file_path, dir_path], self.output_zip_path)

        self.assertTrue(os.path.exists(self.output_zip_path))

        expected_contents = [
            'important.txt',
            'secret_plans/phase1.doc',
            'secret_plans/phase2.doc',
            'MANIFEST.txt'
        ]
        self.assertCountEqual(expected_contents, self._get_zip_contents(self.output_zip_path))

        manifest_content = self._get_zip_file_content(self.output_zip_path, 'MANIFEST.txt')
        self.assertIn("- important.txt", manifest_content)
        self.assertIn("- secret_plans/phase1.doc", manifest_content)
        self.assertIn("- secret_plans/phase2.doc", manifest_content)
        self.assertEqual(len(archived_items), len(expected_contents))

    def test_build_ark_non_existent_source(self):
        non_existent_path = os.path.join(self.base_path, "non_existent_folder")
        with self.assertRaisesRegex(FileNotFoundError, f"Source path '{non_existent_path}' does not exist."):
            build_ark([non_existent_path], self.output_zip_path)
        self.assertFalse(os.path.exists(self.output_zip_path)) # Zip should not be created

    def test_build_ark_empty_source_list(self):
        with self.assertRaisesRegex(ValueError, "No source paths provided to archive."):
            build_ark([], self.output_zip_path)
        self.assertFalse(os.path.exists(self.output_zip_path))

    def test_main_cli_success(self):
        file_path = self._create_dummy_file(os.path.join(self.base_path, "cli_file.txt"))
        
        # Mock rationale: sys.argv is modified for CLI testing.
        # sys.exit is mocked to prevent the test runner from exiting.
        # print is mocked to capture output for verification.
        test_args = ['ark_builder.py', '--source', file_path, '--output', self.output_zip_path]
        with mock.patch('sys.argv', test_args), \
             mock.patch('builtins.print') as mock_print, \
             mock.patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_not_called() # Should not exit on success
            mock_print.assert_any_call(f"Data Ark '{self.output_zip_path}' successfully created with 2 items.")
        
        self.assertTrue(os.path.exists(self.output_zip_path))
        self.assertCountEqual(['cli_file.txt', 'MANIFEST.txt'], self._get_zip_contents(self.output_zip_path))

    def test_main_cli_failure_non_existent_source(self):
        non_existent_path = os.path.join(self.base_path, "cli_non_existent.txt")
        test_args = ['ark_builder.py', '--source', non_existent_path, '--output', self.output_zip_path]
        with mock.patch('sys.argv', test_args), \
             mock.patch('builtins.print') as mock_print, \
             mock.patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_once_with(1) # Should exit with error code 1
            mock_print.assert_any_call(f"Error building Data Ark: Source path '{non_existent_path}' does not exist.", file=sys.stderr)
        self.assertFalse(os.path.exists(self.output_zip_path))

if __name__ == '__main__':
    unittest.main()
