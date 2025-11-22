import unittest
import os
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.sweeper import DigitalDebrisSweeper

class TestDigitalDebrisSweeper(unittest.TestCase):

    def setUp(self):
        # Mock datetime.now() to ensure consistent "current time" for age calculations
        # Mock rationale: `datetime.now()` is non-deterministic and depends on the system clock.
        # We need a fixed reference point to reliably test age-based filtering.
        self.mock_now = datetime(2023, 10, 26, 10, 0, 0)
        self.patcher_datetime_now = patch('src.sweeper.datetime')
        self.mock_datetime = self.patcher_datetime_now.start()
        self.mock_datetime.now.return_value = self.mock_now
        self.mock_datetime.fromtimestamp = datetime.fromtimestamp # Keep original
        self.mock_datetime.timedelta = timedelta # Keep original

        # Mock os.path.isdir to control which paths exist
        # Mock rationale: `os.path.isdir` interacts with the filesystem, making tests non-deterministic
        # and requiring actual file creation. Mocking allows us to simulate directory existence.
        self.patcher_isdir = patch('src.sweeper.os.path.isdir')
        self.mock_isdir = self.patcher_isdir.start()
        self.mock_isdir.return_value = True # Default to existing, override as needed

        # Mock os.path.getmtime to control modification times
        # Mock rationale: `os.path.getmtime` interacts with the filesystem, making tests non-deterministic.
        # We need to control modification times to test the age threshold logic reliably.
        self.patcher_getmtime = patch('src.sweeper.os.path.getmtime')
        self.mock_getmtime = self.patcher_getmtime.start()

        # Mock os.walk to simulate directory structure
        # Mock rationale: `os.walk` traverses the actual filesystem, making tests non-deterministic
        # and requiring complex setup/teardown of temporary directories. Mocking allows us to define
        # a virtual filesystem structure for testing.
        self.patcher_os_walk = patch('src.sweeper.os.walk')
        self.mock_os_walk = self.patcher_os_walk.start()

        # Mock shutil.rmtree to prevent actual file deletion
        # Mock rationale: `shutil.rmtree` performs destructive filesystem operations.
        # Mocking prevents actual deletion, making tests safe, fast, and deterministic.
        self.patcher_rmtree = patch('src.sweeper.shutil.rmtree')
        self.mock_rmtree = self.patcher_rmtree.start()

        # Mock print for cleaner test output
        # Mock rationale: `print` statements pollute test output. Mocking allows us to capture
        # or suppress output during tests.
        self.patcher_print = patch('builtins.print')
        self.mock_print = self.patcher_print.start()

    def tearDown(self):
        self.patcher_datetime_now.stop()
        self.patcher_isdir.stop()
        self.patcher_getmtime.stop()
        self.patcher_os_walk.stop()
        self.patcher_rmtree.stop()
        self.patcher_print.stop()

    def _set_mtime(self, path_mtimes: dict):
        """Helper to set specific modification times for paths."""
        def getmtime_side_effect(path):
            return path_mtimes.get(path, self.mock_now.timestamp())
        self.mock_getmtime.side_effect = getmtime_side_effect

    def test_init_invalid_root_dir(self):
        self.mock_isdir.return_value = False
        with self.assertRaisesRegex(ValueError, "Root directory 'non_existent' does not exist"):
            DigitalDebrisSweeper("non_existent")

    def test_find_no_debris(self):
        self.mock_os_walk.return_value = [
            ("/root", ["src", "docs"], ["file1.txt"]),
            ("/root/src", [], ["main.py"]),
        ]
        sweeper = DigitalDebrisSweeper("/root", age_threshold_days=1)
        debris = sweeper.find_debris()
        self.assertEqual(debris, [])

    def test_find_old_debris(self):
        old_time = self.mock_now - timedelta(days=31)
        self._set_mtime({
            "/root/__pycache__": old_time.timestamp(),
            "/root/node_modules": old_time.timestamp(),
        })
        self.mock_os_walk.return_value = [
            ("/root", ["__pycache__", "node_modules", "src"], ["main.py"]),
            ("/root/src", [], ["app.py"]),
        ]
        sweeper = DigitalDebrisSweeper("/root", age_threshold_days=30)
        debris = sweeper.find_debris()
        self.assertIn("/root/__pycache__", debris)
        self.assertIn("/root/node_modules", debris)
        self.assertEqual(len(debris), 2)

    def test_find_recent_debris_ignored(self):
        recent_time = self.mock_now - timedelta(days=10)
        old_time = self.mock_now - timedelta(days=31)
        self._set_mtime({
            "/root/__pycache__": recent_time.timestamp(),
            "/root/node_modules": old_time.timestamp(),
        })
        self.mock_os_walk.return_value = [
            ("/root", ["__pycache__", "node_modules"], ["main.py"]),
        ]
        sweeper = DigitalDebrisSweeper("/root", age_threshold_days=30)
        debris = sweeper.find_debris()
        self.assertNotIn("/root/__pycache__", debris)
        self.assertIn("/root/node_modules", debris)
        self.assertEqual(len(debris), 1)

    def test_find_multiple_types_of_debris(self):
        old_time = self.mock_now - timedelta(days=40)
        self._set_mtime({
            "/root/__pycache__": old_time.timestamp(),
            "/root/project/node_modules": old_time.timestamp(),
            "/root/another/target": old_time.timestamp(),
        })
        self.mock_os_walk.return_value = [
            ("/root", ["__pycache__", "project", "another"], []),
            ("/root/project", ["node_modules"], []),
            ("/root/another", ["target"], []),
        ]
        sweeper = DigitalDebrisSweeper("/root", age_threshold_days=30)
        debris = sweeper.find_debris()
        self.assertIn("/root/__pycache__", debris)
        self.assertIn("/root/project/node_modules", debris)
        self.assertIn("/root/another/target", debris)
        self.assertEqual(len(debris), 3)

    def test_clean_debris_successful_deletion(self):
        debris_paths = ["/root/old_cache", "/root/another_old_dir"]
        sweeper = DigitalDebrisSweeper("/root", age_threshold_days=1)
        deleted = sweeper.clean_debris(debris_paths)
        self.assertEqual(deleted, debris_paths)
        self.assertEqual(self.mock_rmtree.call_count, 2)
        self.mock_rmtree.assert_any_call("/root/old_cache")
        self.mock_rmtree.assert_any_call("/root/another_old_dir")

    def test_clean_debris_with_deletion_error(self):
        debris_paths = ["/root/old_cache"]
        self.mock_rmtree.side_effect = OSError("Permission denied")
        sweeper = DigitalDebrisSweeper("/root", age_threshold_days=1)
        deleted = sweeper.clean_debris(debris_paths)
        self.assertEqual(deleted, []) # Nothing was successfully deleted
        self.mock_rmtree.assert_called_once_with("/root/old_cache")
        self.mock_print.assert_any_call("Error deleting /root/old_cache: Permission denied")

    def test_clean_debris_path_disappears(self):
        debris_paths = ["/root/old_cache"]
        self.mock_isdir.side_effect = lambda p: p != "/root/old_cache" # Simulate path disappearing
        sweeper = DigitalDebrisSweeper("/root", age_threshold_days=1)
        deleted = sweeper.clean_debris(debris_paths)
        self.assertEqual(deleted, [])
        self.mock_rmtree.assert_not_called()
        self.mock_print.assert_any_call("Warning: Path '/root/old_cache' no longer exists or is not a directory. Skipping.")

    def test_find_debris_does_not_descend_into_debris_dirs(self):
        old_time = self.mock_now - timedelta(days=31)
        self._set_mtime({
            "/root/node_modules": old_time.timestamp(),
            "/root/node_modules/sub_module": old_time.timestamp(), # Should not be found separately
        })
        self.mock_os_walk.return_value = [
            ("/root", ["node_modules", "src"], []),
            ("/root/node_modules", ["sub_module"], []), # This should be skipped by os.walk logic
            ("/root/src", [], []),
        ]
        sweeper = DigitalDebrisSweeper("/root", age_threshold_days=30)
        debris = sweeper.find_debris()
        self.assertEqual(debris, ["/root/node_modules"])
        # Ensure os.walk was called in a way that prevents descending into node_modules
        # This is implicitly tested by the result, as sub_module is not found.
        # The internal logic of `find_debris` modifies `dirs` in place to prevent further descent.

    def test_different_age_threshold(self):
        old_enough_for_10_days = self.mock_now - timedelta(days=11)
        not_old_enough_for_30_days = self.mock_now - timedelta(days=20)
        self._set_mtime({
            "/root/cache_10d": old_enough_for_10_days.timestamp(),
            "/root/cache_30d": not_old_enough_for_30_days.timestamp(),
        })
        self.mock_os_walk.return_value = [
            ("/root", ["cache_10d", "cache_30d"], []),
        ]
        # Test with 10-day threshold
        sweeper_10d = DigitalDebrisSweeper("/root", age_threshold_days=10)
        debris_10d = sweeper_10d.find_debris()
        self.assertIn("/root/cache_10d", debris_10d)
        self.assertIn("/root/cache_30d", debris_10d) # Both are older than 10 days
        self.assertEqual(len(debris_10d), 2)

        # Test with 30-day threshold
        sweeper_30d = DigitalDebrisSweeper("/root", age_threshold_days=30)
        debris_30d = sweeper_30d.find_debris()
        self.assertIn("/root/cache_10d", debris_30d) # Still older than 30 days
        self.assertNotIn("/root/cache_30d", debris_30d) # Not older than 30 days
        self.assertEqual(len(debris_30d), 1)
