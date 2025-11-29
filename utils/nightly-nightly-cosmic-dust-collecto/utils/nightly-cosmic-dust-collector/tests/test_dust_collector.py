import unittest
import os
from unittest.mock import patch, MagicMock
from src.dust_collector import find_cosmic_dust

class TestCosmicDustCollector(unittest.TestCase):

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_empty_directory(self, mock_getsize, mock_isfile, mock_walk):
        # Mock rationale: Simulate an empty directory structure.
        # os.walk will yield nothing, os.path.isfile and os.path.getsize won't be called.
        mock_walk.return_value = []
        result = find_cosmic_dust("/mock/path")
        self.assertEqual(result, [])
        mock_walk.assert_called_once_with("/mock/path")

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_no_dust_files(self, mock_getsize, mock_isfile, mock_walk):
        # Mock rationale: Simulate a directory with only large files.
        # os.walk yields files, os.path.isfile confirms they are files,
        # but os.path.getsize returns values above the threshold.
        mock_walk.return_value = [
            ("/mock/path", ["subdir"], ["large_file1.txt", "large_file2.log"]),
            ("/mock/path/subdir", [], ["another_large.py"])
        ]
        mock_isfile.return_value = True
        mock_getsize.side_effect = [2000, 3000, 1500] # All > 1024 threshold

        result = find_cosmic_dust("/mock/path", threshold_bytes=1024)
        self.assertEqual(result, [])
        self.assertEqual(mock_getsize.call_count, 3) # Ensure sizes were checked

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_with_dust_files(self, mock_getsize, mock_isfile, mock_walk):
        # Mock rationale: Simulate a directory with a mix of large and small files.
        # os.walk yields files, os.path.isfile confirms they are files,
        # os.path.getsize returns values, some of which are below the threshold.
        mock_walk.return_value = [
            ("/mock/path", ["subdir"], ["small.txt", "large.log", "empty.csv"]),
            ("/mock/path/subdir", [], ["another_small.py"])
        ]
        mock_isfile.return_value = True
        # Sizes for: small.txt, large.log, empty.csv, another_small.py
        mock_getsize.side_effect = [100, 2000, 0, 500]

        expected_dust = [
            (os.path.join("/mock/path", "small.txt"), 100),
            (os.path.join("/mock/path", "empty.csv"), 0),
            (os.path.join("/mock/path/subdir", "another_small.py"), 500)
        ]

        result = find_cosmic_dust("/mock/path", threshold_bytes=1024)
        self.assertCountEqual(result, expected_dust) # Use assertCountEqual for order-independent comparison
        self.assertEqual(mock_getsize.call_count, 4)

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_with_empty_files(self, mock_getsize, mock_isfile, mock_walk):
        # Mock rationale: Specifically test for empty files (size 0).
        # os.walk yields files, os.path.isfile confirms they are files,
        # os.path.getsize returns 0 for some files.
        mock_walk.return_value = [
            ("/mock/path", [], ["empty1.txt", "not_empty.log", "empty2.csv"])
        ]
        mock_isfile.return_value = True
        mock_getsize.side_effect = [0, 5000, 0] # empty1, not_empty, empty2

        expected_dust = [
            (os.path.join("/mock/path", "empty1.txt"), 0),
            (os.path.join("/mock/path", "empty2.csv"), 0)
        ]

        result = find_cosmic_dust("/mock/path", threshold_bytes=1024)
        self.assertCountEqual(result, expected_dust)
        self.assertEqual(mock_getsize.call_count, 3)

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_ignored_directories(self, mock_getsize, mock_isfile, mock_walk):
        # Mock rationale: Ensure that files within ignored directories are not processed.
        # os.walk is mocked to include ignored directories, but the find_cosmic_dust
        # function should filter them out before processing their contents.
        mock_walk.return_value = [
            ("/mock/path", [".git", "src", "__pycache__"], ["root_file.txt"]),
            (os.path.join("/mock/path", ".git"), [], ["config"]), # Should be ignored
            (os.path.join("/mock/path", "src"), [], ["source.py"]),
            (os.path.join("/mock/path", "__pycache__"), [], ["cache.pyc"]) # Should be ignored
        ]
        mock_isfile.return_value = True
        # Sizes for: root_file.txt, source.py
        mock_getsize.side_effect = [50, 100] # Both are dust

        expected_dust = [
            (os.path.join("/mock/path", "root_file.txt"), 50),
            (os.path.join("/mock/path", "src", "source.py"), 100)
        ]

        result = find_cosmic_dust("/mock/path", threshold_bytes=1024)
        self.assertCountEqual(result, expected_dust)
        # Only root_file.txt and source.py should have their sizes checked
        self.assertEqual(mock_getsize.call_count, 2)
        # Verify that os.walk was called with the correct path
        mock_walk.assert_called_once_with("/mock/path")

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_os_error_handling(self, mock_getsize, mock_isfile, mock_walk):
        # Mock rationale: Simulate an OSError (e.g., permission denied, broken symlink)
        # when trying to get file size. The utility should gracefully skip such files.
        mock_walk.return_value = [
            ("/mock/path", [], ["good_file.txt", "bad_file.txt"])
        ]
        mock_isfile.return_value = True
        # good_file.txt size is 50, bad_file.txt raises OSError
        mock_getsize.side_effect = [50, OSError("Permission denied")]

        expected_dust = [
            (os.path.join("/mock/path", "good_file.txt"), 50)
        ]

        result = find_cosmic_dust("/mock/path", threshold_bytes=1024)
        self.assertCountEqual(result, expected_dust)
        self.assertEqual(mock_getsize.call_count, 2) # Both attempts to get size should happen

    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_threshold_variation(self, mock_getsize, mock_isfile, mock_walk):
        # Mock rationale: Test with a different threshold to ensure it's respected.
        mock_walk.return_value = [
            ("/mock/path", [], ["small.txt", "medium.txt", "large.txt"])
        ]
        mock_isfile.return_value = True
        # Sizes: small=100, medium=500, large=1500
        mock_getsize.side_effect = [100, 500, 1500]

        # Test with threshold 200
        result_200 = find_cosmic_dust("/mock/path", threshold_bytes=200)
        expected_200 = [(os.path.join("/mock/path", "small.txt"), 100)]
        self.assertCountEqual(result_200, expected_200)
        self.assertEqual(mock_getsize.call_count, 3) # Reset for next call

        # Test with threshold 600
        mock_getsize.side_effect = [100, 500, 1500] # Reset side_effect for second call
        result_600 = find_cosmic_dust("/mock/path", threshold_bytes=600)
        expected_600 = [
            (os.path.join("/mock/path", "small.txt"), 100),
            (os.path.join("/mock/path", "medium.txt"), 500)
        ]
        self.assertCountEqual(result_600, expected_600)
        self.assertEqual(mock_getsize.call_count, 6) # 3 from first, 3 from second

if __name__ == "__main__":
    unittest.main()
