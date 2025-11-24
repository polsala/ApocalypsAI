import unittest
import os
import shutil
import tempfile
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Import the functions to test
from src.duster import find_dust_bunnies, delete_dust_bunnies, is_old_enough, DIR_PATTERNS, FILE_PATTERNS

class TestDuster(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_dir = tempfile.mkdtemp()
        self.old_date = (datetime.now() - timedelta(days=10)).timestamp()
        self.new_date = (datetime.now() - timedelta(days=1)).timestamp()

        # Create various "dust bunnies" and regular files/dirs
        os.makedirs(os.path.join(self.test_dir, "project_a", "__pycache__"))
        os.makedirs(os.path.join(self.test_dir, "project_a", "src"))
        with open(os.path.join(self.test_dir, "project_a", "src", "main.py"), "w") as f:
            f.write("print('hello')")

        os.makedirs(os.path.join(self.test_dir, "project_b", "node_modules"))
        with open(os.path.join(self.test_dir, "project_b", "package.json"), "w") as f:
            f.write("{}")

        os.makedirs(os.path.join(self.test_dir, "project_c", "target"))
        with open(os.path.join(self.test_dir, "project_c", "target", "app.jar"), "w") as f:
            f.write("jar_content")

        os.makedirs(os.path.join(self.test_dir, "project_d"))
        with open(os.path.join(self.test_dir, "project_d", ".DS_Store"), "w") as f:
            f.write("mac_junk")
        with open(os.path.join(self.test_dir, "project_d", "Thumbs.db"), "w") as f:
            f.write("win_junk")
        with open(os.path.join(self.test_dir, "project_d", "tempfile.tmp"), "w") as f:
            f.write("tmp_content")
        os.utime(os.path.join(self.test_dir, "project_d", "tempfile.tmp"), (self.old_date, self.old_date))
        with open(os.path.join(self.test_dir, "project_d", "newfile.tmp"), "w") as f:
            f.write("new_tmp_content")
        os.utime(os.path.join(self.test_dir, "project_d", "newfile.tmp"), (self.new_date, self.new_date))

        with open(os.path.join(self.test_dir, "project_d", "old.log"), "w") as f:
            f.write("old log content")
        os.utime(os.path.join(self.test_dir, "project_d", "old.log"), (self.old_date, self.old_date))
        with open(os.path.join(self.test_dir, "project_d", "new.log"), "w") as f:
            f.write("new log content")
        os.utime(os.path.join(self.test_dir, "project_d", "new.log"), (self.new_date, self.new_date))

        # Create a non-dust bunny directory
        os.makedirs(os.path.join(self.test_dir, "important_data"))
        with open(os.path.join(self.test_dir, "important_data", "data.txt"), "w") as f:
            f.write("important stuff")

        # Create a nested dust bunny
        os.makedirs(os.path.join(self.test_dir, "nested_project", "build", "intermediate"))
        with open(os.path.join(self.test_dir, "nested_project", "build", "intermediate", "file.o"), "w") as f:
            f.write("obj_file")

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def test_is_old_enough(self):
        # Mock rationale: os.path.getmtime is a system call that depends on file system state.
        # Mocking it allows deterministic testing of the age logic without actual file modification.
        with patch('os.path.getmtime', return_value=(datetime.now() - timedelta(days=10)).timestamp()):
            self.assertTrue(is_old_enough("dummy_path", 7))
            self.assertFalse(is_old_enough("dummy_path", 15))
            self.assertTrue(is_old_enough("dummy_path", 0)) # 0 days means no age limit

        with patch('os.path.getmtime', return_value=(datetime.now() - timedelta(days=5)).timestamp()):
            self.assertFalse(is_old_enough("dummy_path", 7))
            self.assertTrue(is_old_enough("dummy_path", 0))

        # Test with non-existent file (should return False)
        with patch('os.path.getmtime', side_effect=OSError):
            self.assertFalse(is_old_enough("non_existent_path", 7))


    def test_find_dust_bunnies_default_age(self):
        # Default age_days is 7
        found_bunnies = find_dust_bunnies(self.test_dir)
        found_bunnies_set = set(found_bunnies)

        expected_bunnies = [
            os.path.join(self.test_dir, "project_a", "__pycache__"),
            os.path.join(self.test_dir, "project_b", "node_modules"),
            os.path.join(self.test_dir, "project_c", "target"),
            os.path.join(self.test_dir, "project_d", ".DS_Store"),
            os.path.join(self.test_dir, "project_d", "Thumbs.db"),
            os.path.join(self.test_dir, "project_d", "tempfile.tmp"), # Older than 7 days
            os.path.join(self.test_dir, "project_d", "old.log"),      # Older than 7 days
            os.path.join(self.test_dir, "nested_project", "build"),
        ]

        # Ensure all expected bunnies are found
        for bunny in expected_bunnies:
            self.assertIn(bunny, found_bunnies_set, f"Expected {bunny} not found.")

        # Ensure new.log and newfile.tmp are NOT found (they are only 1 day old)
        self.assertNotIn(os.path.join(self.test_dir, "project_d", "new.log"), found_bunnies_set)
        self.assertNotIn(os.path.join(self.test_dir, "project_d", "newfile.tmp"), found_bunnies_set)

        # Ensure important_data is NOT found
        self.assertNotIn(os.path.join(self.test_dir, "important_data"), found_bunnies_set)
        self.assertNotIn(os.path.join(self.test_dir, "important_data", "data.txt"), found_bunnies_set)

        # Check total count (might vary slightly based on OS and exact patterns, but should be close)
        self.assertEqual(len(found_bunnies_set), len(expected_bunnies))


    def test_find_dust_bunnies_no_age_limit(self):
        # Set age_days to 0, so all log/tmp files are considered
        found_bunnies = find_dust_bunnies(self.test_dir, age_days=0)
        found_bunnies_set = set(found_bunnies)

        expected_bunnies = [
            os.path.join(self.test_dir, "project_a", "__pycache__"),
            os.path.join(self.test_dir, "project_b", "node_modules"),
            os.path.join(self.test_dir, "project_c", "target"),
            os.path.join(self.test_dir, "project_d", ".DS_Store"),
            os.path.join(self.test_dir, "project_d", "Thumbs.db"),
            os.path.join(self.test_dir, "project_d", "tempfile.tmp"),
            os.path.join(self.test_dir, "project_d", "newfile.tmp"), # Now included
            os.path.join(self.test_dir, "project_d", "old.log"),
            os.path.join(self.test_dir, "project_d", "new.log"),      # Now included
            os.path.join(self.test_dir, "nested_project", "build"),
        ]

        for bunny in expected_bunnies:
            self.assertIn(bunny, found_bunnies_set, f"Expected {bunny} not found with age_days=0.")

        self.assertEqual(len(found_bunnies_set), len(expected_bunnies))

    def test_delete_dust_bunnies(self):
        # Find bunnies first
        bunnies_to_delete = find_dust_bunnies(self.test_dir, age_days=0)
        self.assertGreater(len(bunnies_to_delete), 0)

        # Ensure some files/dirs exist before deletion
        for bunny_path in bunnies_to_delete:
            self.assertTrue(os.path.exists(bunny_path))

        # Perform deletion
        delete_dust_bunnies(bunnies_to_delete)

        # Verify that all found bunnies are now deleted
        for bunny_path in bunnies_to_delete:
            self.assertFalse(os.path.exists(bunny_path), f"Path {bunny_path} should have been deleted but still exists.")

        # Verify that non-dust bunny files still exist
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "project_a", "src", "main.py")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "project_b", "package.json")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "important_data", "data.txt")))

    def test_delete_dust_bunnies_empty_list(self):
        # Mock rationale: print is a side effect. Mocking it allows verifying that
        # the expected message is printed when no items are passed for deletion.
        with patch('builtins.print') as mock_print:
            delete_dust_bunnies([])
            mock_print.assert_any_call("No dust bunnies to delete. Your digital space is sparkling!")

    def test_find_dust_bunnies_invalid_path(self):
        # Mock rationale: print is a side effect. Mocking it allows verifying that
        # the expected error message is printed for an invalid path.
        with patch('builtins.print') as mock_print:
            found = find_dust_bunnies("/non/existent/path")
            self.assertEqual(found, [])
            mock_print.assert_any_call("Error: Path '/non/existent/path' is not a valid directory.")

    def test_delete_dust_bunnies_os_error(self):
        # Mock rationale: os.remove and shutil.rmtree are system calls.
        # Mocking them to raise an OSError simulates permission issues or other
        # unexpected errors during deletion, allowing testing of error handling.
        mock_path = os.path.join(self.test_dir, "unremovable_file.txt")
        with open(mock_path, "w") as f:
            f.write("content")

        with patch('os.remove', side_effect=OSError("Permission denied")):
            with patch('shutil.rmtree', side_effect=OSError("Permission denied")):
                with patch('builtins.print') as mock_print:
                    delete_dust_bunnies([mock_path, os.path.join(self.test_dir, "project_a", "__pycache__")])
                    mock_print.assert_any_call(f"  Error deleting '{mock_path}': Permission denied")
                    mock_print.assert_any_call(f"  Error deleting '{os.path.join(self.test_dir, 'project_a', '__pycache__')}': Permission denied")

        # The files should still exist because deletion failed
        self.assertTrue(os.path.exists(mock_path))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "project_a", "__pycache__")))
