import unittest
import os
import shutil
from pathlib import Path
import tempfile
from unittest.mock import patch
import sys

# Add the src directory to the Python path to import collector.py
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from collector import find_empty_directories, collect_dust_bunnies, main

class TestCosmicDustBunnyCollector(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_path = self.temp_dir / "test_root"
        self.test_path.mkdir()

        # Create a test directory structure
        # Empty directories
        (self.test_path / "empty_dir_1").mkdir()
        (self.test_path / "empty_dir_2").mkdir()
        (self.test_path / "nested" / "empty_nested_1").mkdir(parents=True)
        (self.test_path / "nested" / "empty_nested_2").mkdir() # This will be created by parents=True above

        # Non-empty directories
        (self.test_path / "non_empty_dir_1").mkdir()
        (self.test_path / "non_empty_dir_1" / "file.txt").touch()
        (self.test_path / "non_empty_dir_2").mkdir()
        (self.test_path / "non_empty_dir_2" / "sub_dir").mkdir()
        (self.test_path / "nested" / "non_empty_nested").mkdir()
        (self.test_path / "nested" / "non_empty_nested" / "another_file.log").touch()

        # Directory that becomes empty after deleting a file
        (self.test_path / "temp_empty").mkdir()
        (self.test_path / "temp_empty" / "temp_file.tmp").touch()

        self.expected_empty_dirs = sorted([
            self.test_path / "empty_dir_1",
            self.test_path / "empty_dir_2",
            self.test_path / "nested" / "empty_nested_1",
            self.test_path / "nested" / "empty_nested_2",
        ])

    def tearDown(self):
        # Clean up the temporary directory
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_find_empty_directories(self):
        """
        Test that find_empty_directories correctly identifies all empty directories.
        # Mock rationale: No mocks needed. Using tempfile.TemporaryDirectory provides a real, isolated, and deterministic file system for testing.
        """
        found_empty = sorted(find_empty_directories(self.test_path))
        self.assertEqual(found_empty, self.expected_empty_dirs)

        # Test with a path that has no empty directories
        no_empty_path = self.temp_dir / "no_empty"
        no_empty_path.mkdir()
        (no_empty_path / "file.txt").touch()
        self.assertEqual(find_empty_directories(no_empty_path), [])

        # Test with a non-existent path
        self.assertEqual(find_empty_directories(self.temp_dir / "non_existent"), [])

    def test_collect_dust_bunnies_no_delete(self):
        """
        Test that collect_dust_bunnies lists empty directories without deleting them.
        # Mock rationale: No mocks needed. Using tempfile.TemporaryDirectory provides a real, isolated, and deterministic file system for testing.
        """
        initial_state = {p: p.exists() for p in self.expected_empty_dirs}
        
        # Capture stdout to check printed messages
        with patch('sys.stdout', new_callable=self._mock_stdout) as mock_stdout:
            found_dirs = collect_dust_bunnies(self.test_path, delete=False)
            output = mock_stdout.getvalue()

        self.assertEqual(sorted(found_dirs), self.expected_empty_dirs)
        for p in self.expected_empty_dirs:
            self.assertTrue(p.exists(), f"Directory {p} should still exist.")
            self.assertIn(str(p), output)
        self.assertIn("To collect these dust bunnies, run with the --delete flag.", output)
        self.assertNotIn("Collected:", output)

    def test_collect_dust_bunnies_with_delete(self):
        """
        Test that collect_dust_bunnies correctly deletes empty directories.
        # Mock rationale: No mocks needed. Using tempfile.TemporaryDirectory provides a real, isolated, and deterministic file system for testing.
        """
        # First, ensure the 'temp_empty' directory is not empty
        self.assertTrue((self.test_path / "temp_empty" / "temp_file.tmp").exists())
        
        # Now delete the file, making 'temp_empty' an empty directory
        os.remove(self.test_path / "temp_empty" / "temp_file.tmp")
        self.expected_empty_dirs.append(self.test_path / "temp_empty")
        self.expected_empty_dirs = sorted(self.expected_empty_dirs)

        # Capture stdout to check printed messages
        with patch('sys.stdout', new_callable=self._mock_stdout) as mock_stdout:
            deleted_dirs = collect_dust_bunnies(self.test_path, delete=True)
            output = mock_stdout.getvalue()

        self.assertEqual(sorted(deleted_dirs), self.expected_empty_dirs)
        for p in self.expected_empty_dirs:
            self.assertFalse(p.exists(), f"Directory {p} should have been deleted.")
            self.assertIn(f"Collected: {p}", output)

        # Ensure non-empty directories are still there
        self.assertTrue((self.test_path / "non_empty_dir_1").exists())
        self.assertTrue((self.test_path / "non_empty_dir_1" / "file.txt").exists())
        self.assertTrue((self.test_path / "non_empty_dir_2").exists())
        self.assertTrue((self.test_path / "non_empty_dir_2" / "sub_dir").exists())

    def test_collect_dust_bunnies_no_empty_dirs(self):
        """
        Test behavior when no empty directories are found.
        # Mock rationale: No mocks needed. Using tempfile.TemporaryDirectory provides a real, isolated, and deterministic file system for testing.
        """
        # Create a new temp dir with no empty directories
        temp_dir_no_empty = Path(tempfile.mkdtemp())
        (temp_dir_no_empty / "root").mkdir()
        (temp_dir_no_empty / "root" / "file.txt").touch()
        (temp_dir_no_empty / "root" / "sub").mkdir()
        (temp_dir_no_empty / "root" / "sub" / "file2.txt").touch()

        with patch('sys.stdout', new_callable=self._mock_stdout) as mock_stdout:
            found_dirs = collect_dust_bunnies(temp_dir_no_empty / "root", delete=False)
            output = mock_stdout.getvalue()

        self.assertEqual(found_dirs, [])
        self.assertIn("No cosmic dust bunnies found!", output)
        shutil.rmtree(temp_dir_no_empty)

    def test_collect_dust_bunnies_invalid_path(self):
        """
        Test behavior with an invalid or non-existent path.
        # Mock rationale: No mocks needed. Using tempfile.TemporaryDirectory provides a real, isolated, and deterministic file system for testing.
        """
        non_existent_path = self.temp_dir / "does_not_exist"
        with patch('sys.stdout', new_callable=self._mock_stdout) as mock_stdout:
            found_dirs = collect_dust_bunnies(non_existent_path, delete=False)
            output = mock_stdout.getvalue()

        self.assertEqual(found_dirs, [])
        self.assertIn(f"Error: Path '{non_existent_path}' is not a valid directory.", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=self._mock_stdout)
    def test_main_no_delete(self, mock_stdout, mock_parse_args):
        """
        Test the main function with --path and no --delete.
        # Mock rationale:
        # - argparse.ArgumentParser.parse_args: To simulate command-line arguments without actually running the script from CLI.
        # - sys.stdout: To capture and inspect the output printed to the console.
        """
        mock_parse_args.return_value = argparse.Namespace(
            path=str(self.test_path),
            delete=False
        )
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Found 4 cosmic dust bunnies:", output)
        self.assertIn("To collect these dust bunnies, run with the --delete flag.", output)
        self.assertTrue((self.test_path / "empty_dir_1").exists()) # Should still exist
        self.assertTrue((self.test_path / "empty_dir_1").is_dir()) # Should still exist

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=self._mock_stdout)
    def test_main_with_delete(self, mock_stdout, mock_parse_args):
        """
        Test the main function with --path and --delete.
        # Mock rationale:
        # - argparse.ArgumentParser.parse_args: To simulate command-line arguments without actually running the script from CLI.
        # - sys.stdout: To capture and inspect the output printed to the console.
        """
        # Make 'temp_empty' an empty directory for this test
        os.remove(self.test_path / "temp_empty" / "temp_file.tmp")
        
        mock_parse_args.return_value = argparse.Namespace(
            path=str(self.test_path),
            delete=True
        )
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Initiating dust bunny collection protocol...", output)
        self.assertIn("Successfully collected 5 cosmic dust bunnies.", output) # 4 from setup + 1 temp_empty
        self.assertFalse((self.test_path / "empty_dir_1").exists()) # Should be deleted

    # Helper to mock stdout
    class _mock_stdout:
        def __init__(self):
            self._buffer = []
        def write(self, s):
            self._buffer.append(s)
        def flush(self):
            pass
        def getvalue(self):
            return "".join(self._buffer)

if __name__ == '__main__':
    unittest.main()
