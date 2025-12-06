import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from io import StringIO

# A simple way to import from a sibling directory 'src' for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cache_cleaner import find_and_clean_caches, get_dir_size, format_bytes, CACHE_PATTERNS
sys.path.pop(0)

class TestCacheCleaner(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_caches_no_delete(self, mock_stdout, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with cache directories
        mock_isdir.return_value = True
        mock_walk.side_effect = [
            # First call for root_dir
            ('/project', ['src', 'node_modules', '__pycache__', 'build'], ['main.py']),
            # Second call for 'src' (should be skipped as it's not a cache)
            ('/project/src', [], ['helper.py']),
            # Subsequent calls for 'node_modules', '__pycache__', 'build' should be prevented by logic in find_and_clean_caches
        ]
        # Mock rationale: Simulate file sizes for accurate size calculation
        mock_getsize.side_effect = [100, 50000000, 2000000, 100000000] # main.py, node_modules content, __pycache__ content, build content

        find_and_clean_caches('/project', delete_mode=False)

        output = mock_stdout.getvalue()
        self.assertIn("Scanning '/project' for digital debris...", output)
        self.assertIn("--- Digital Debris Report ---", output)
        self.assertIn("  - /project/node_modules", output)
        self.assertIn("  - /project/__pycache__", output)
        self.assertIn("  - /project/build", output)
        self.assertIn("Total reclaimable space: ", output)
        self.assertIn("Run with '--delete' to reclaim this space.", output)
        self.assertNotIn("Proceed with deletion", output)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('shutil.rmtree')
    @patch('builtins.input', return_value='y') # Mock rationale: Simulate user confirming deletion
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_caches_with_delete_confirmed(self, mock_stdout, mock_input, mock_rmtree, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with cache directories
        mock_isdir.return_value = True
        mock_walk.side_effect = [
            ('/project', ['src', 'node_modules', '__pycache__'], ['main.py']),
            ('/project/src', [], ['helper.py']),
        ]
        # Mock rationale: Simulate file sizes
        mock_getsize.side_effect = [100, 50000000, 2000000] # main.py, node_modules content, __pycache__ content

        find_and_clean_caches('/project', delete_mode=True)

        output = mock_stdout.getvalue()
        self.assertIn("Scanning '/project' for digital debris...", output)
        self.assertIn("Total reclaimable space: ", output)
        self.assertIn("Proceed with deletion of all identified caches? (y/N): ", output)
        self.assertIn("Initiating digital resource conservation protocol...", output)
        self.assertIn("  Deleted: /project/node_modules", output)
        self.assertIn("  Deleted: /project/__pycache__", output)
        self.assertIn("Digital resources conserved. Stay vigilant!", output)
        # Mock rationale: Verify rmtree was called for each cache directory
        mock_rmtree.assert_any_call('/project/node_modules')
        mock_rmtree.assert_any_call('/project/__pycache__')
        self.assertEqual(mock_rmtree.call_count, 2)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('shutil.rmtree')
    @patch('builtins.input', return_value='n') # Mock rationale: Simulate user declining deletion
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_caches_with_delete_declined(self, mock_stdout, mock_input, mock_rmtree, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with cache directories
        mock_isdir.return_value = True
        mock_walk.side_effect = [
            ('/project', ['node_modules'], ['main.py']),
        ]
        # Mock rationale: Simulate file sizes
        mock_getsize.side_effect = [100, 50000000] # main.py, node_modules content

        find_and_clean_caches('/project', delete_mode=True)

        output = mock_stdout.getvalue()
        self.assertIn("Proceed with deletion of all identified caches? (y/N): ", output)
        self.assertIn("Deletion aborted. Digital debris remains. Proceed with caution.", output)
        # Mock rationale: Verify rmtree was NOT called
        mock_rmtree.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('sys.stdout', new_callable=StringIO)
    def test_no_caches_found(self, mock_stdout, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with no cache directories
        mock_isdir.return_value = True
        mock_walk.side_effect = [
            ('/project', ['src', 'docs'], ['main.py', 'README.md']),
            ('/project/src', [], ['helper.py']),
            ('/project/docs', [], ['index.html']),
        ]

        find_and_clean_caches('/project', delete_mode=False)

        output = mock_stdout.getvalue()
        self.assertIn("No digital debris found. Your project is lean and mean!", output)
        self.assertNotIn("Total reclaimable space", output)

    @patch('os.path.isdir')
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_root_dir(self, mock_stdout, mock_isdir):
        # Mock rationale: Simulate an invalid root directory
        mock_isdir.return_value = False

        find_and_clean_caches('/nonexistent', delete_mode=False)

        output = mock_stdout.getvalue()
        self.assertIn("Error: Directory '/nonexistent' not found.", output)

    @patch('os.walk')
    @patch('os.path.getsize')
    def test_get_dir_size(self, mock_getsize, mock_walk):
        # Mock rationale: Simulate a directory structure for size calculation
        mock_walk.side_effect = [
            ('/test_dir', ['subdir'], ['file1.txt', 'file2.log']),
            ('/test_dir/subdir', [], ['subfile.py'])
        ]
        # Mock rationale: Simulate file sizes
        mock_getsize.side_effect = [100, 200, 50]

        size = get_dir_size('/test_dir')
        self.assertEqual(size, 350)
        self.assertEqual(mock_getsize.call_count, 3)

    def test_format_bytes(self):
        self.assertEqual(format_bytes(100), "100.00 B")
        self.assertEqual(format_bytes(1024), "1.00 KB")
        self.assertEqual(format_bytes(1024 * 1024 * 1.5), "1.50 MB")
        self.assertEqual(format_bytes(1024 * 1024 * 1024 * 2.75), "2.75 GB")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('shutil.rmtree')
    @patch('builtins.input', return_value='y')
    @patch('sys.stdout', new_callable=StringIO)
    def test_rmtree_error_handling(self, mock_stdout, mock_input, mock_rmtree, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with a cache directory
        mock_isdir.return_value = True
        mock_walk.side_effect = [
            ('/project', ['node_modules'], ['main.py']),
        ]
        # Mock rationale: Simulate file sizes
        mock_getsize.side_effect = [100, 50000000]
        # Mock rationale: Simulate an OSError during rmtree call
        mock_rmtree.side_effect = OSError("Permission denied")

        find_and_clean_caches('/project', delete_mode=True)

        output = mock_stdout.getvalue()
        self.assertIn("Error deleting /project/node_modules: Permission denied", output)
        mock_rmtree.assert_called_once_with('/project/node_modules')

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('sys.stdout', new_callable=StringIO)
    def test_nested_cache_dirs_handled_correctly(self, mock_stdout, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with nested cache directories
        mock_isdir.return_value = True
        mock_walk.side_effect = [
            ('/project', ['src', 'node_modules'], ['main.py']),
            ('/project/src', ['__pycache__'], ['app.py']),
            ('/project/src/__pycache__', [], ['app.cpython-39.pyc']),
            # os.walk should not descend into node_modules or __pycache__ after they are identified
        ]
        # Mock rationale: Simulate file sizes
        mock_getsize.side_effect = [100, 50000000, 200, 1000000] # main.py, node_modules content, app.py, __pycache__ content

        find_and_clean_caches('/project', delete_mode=False)

        output = mock_stdout.getvalue()
        self.assertIn("  - /project/node_modules", output)
        self.assertIn("  - /project/src/__pycache__", output)
        self.assertIn("Total reclaimable space: ", output)
        # Ensure os.walk was called for /project and /project/src, but not for the identified caches themselves
        # The logic in find_and_clean_caches modifies `dirnames` to prevent further descent.
        # This test primarily checks the output and that the correct caches are identified.
        self.assertEqual(len([c for c in output.split('\n') if '  -' in c]), 2) # Expect 2 cache dirs reported


if __name__ == '__main__':
    unittest.main()
