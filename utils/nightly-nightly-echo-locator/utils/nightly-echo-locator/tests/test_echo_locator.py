import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import io
import json

# Add the src directory to the path to allow importing echo_locator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from echo_locator import find_duplicate_files, calculate_sha256, main
sys.path.pop(0)

class TestEchoLocator(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize')
    def test_calculate_sha256(self, mock_getsize, mock_open_func):
        # Mock rationale: `calculate_sha256` reads file content. We need to simulate file content
        # without actually creating files on disk, ensuring deterministic and offline tests.
        # `mock_open` allows us to control what `open()` returns, and `mock_getsize` is needed
        # for `find_duplicate_files` later, though not directly by `calculate_sha256`.

        mock_file_content = b"test content for hashing"
        mock_open_func.return_value.read.side_effect = [mock_file_content, b'']
        mock_getsize.return_value = len(mock_file_content)

        expected_hash = hashlib.sha256(mock_file_content).hexdigest()
        actual_hash = calculate_sha256("/fake/path/to/file.txt")

        self.assertEqual(actual_hash, expected_hash)
        mock_open_func.assert_called_once_with("/fake/path/to/file.txt", 'rb')

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir', return_value=True)
    def test_find_duplicate_files_no_duplicates(self, mock_isdir, mock_open_func, mock_getsize, mock_walk):
        # Mock rationale: `find_duplicate_files` interacts heavily with the filesystem (`os.walk`, `os.path.getsize`, `open`).
        # We mock these to create a virtual filesystem structure and control file contents and sizes,
        # ensuring the test is isolated, fast, and deterministic.

        # Simulate a directory structure with unique files
        mock_walk.return_value = [
            ('/dir1', [], ['fileA.txt', 'fileB.txt']),
        ]

        # Define file contents and sizes for hashing
        file_contents = {
            '/dir1/fileA.txt': b'content A',
            '/dir1/fileB.txt': b'content B',
        }
        mock_getsize.side_effect = lambda p: len(file_contents.get(p, b''))
        
        # Mock open to return content based on path
        def mock_open_side_effect(filepath, mode='r'):
            if 'b' in mode:
                return io.BytesIO(file_contents.get(filepath, b''))
            return io.StringIO(file_contents.get(filepath, b'').decode())
        mock_open_func.side_effect = mock_open_side_effect

        duplicates = find_duplicate_files(['/dir1'])
        self.assertEqual(duplicates, {})

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir', return_value=True)
    def test_find_duplicate_files_with_duplicates(self, mock_isdir, mock_open_func, mock_getsize, mock_walk):
        # Mock rationale: Same as above, but specifically to test the detection of duplicate files.
        # We set up a scenario where two files have identical content and size.

        # Simulate a directory structure with duplicate files
        mock_walk.return_value = [
            ('/dir1', [], ['file1.txt', 'file2.txt']),
            ('/dir2', [], ['file3.txt'])
        ]

        # Define file contents and sizes
        file_contents = {
            '/dir1/file1.txt': b'duplicate content',
            '/dir1/file2.txt': b'unique content',
            '/dir2/file3.txt': b'duplicate content',
        }
        mock_getsize.side_effect = lambda p: len(file_contents.get(p, b''))

        def mock_open_side_effect(filepath, mode='r'):
            if 'b' in mode:
                return io.BytesIO(file_contents.get(filepath, b''))
            return io.StringIO(file_contents.get(filepath, b'').decode())
        mock_open_func.side_effect = mock_open_side_effect

        expected_hash = hashlib.sha256(b'duplicate content').hexdigest()
        duplicates = find_duplicate_files(['/dir1', '/dir2'])

        self.assertIn(expected_hash, duplicates)
        self.assertCountEqual(duplicates[expected_hash], ['/dir1/file1.txt', '/dir2/file3.txt'])
        self.assertEqual(len(duplicates), 1)

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir', return_value=True)
    def test_find_duplicate_files_min_size(self, mock_isdir, mock_open_func, mock_getsize, mock_walk):
        # Mock rationale: Test the `min_size` filtering. We simulate files with different sizes
        # and ensure only those meeting the minimum size requirement are processed.

        mock_walk.return_value = [
            ('/data', [], ['small.txt', 'medium.txt', 'large.txt']),
        ]

        file_contents = {
            '/data/small.txt': b's',
            '/data/medium.txt': b'm' * 100,
            '/data/large.txt': b'l' * 1000,
        }
        mock_getsize.side_effect = lambda p: len(file_contents.get(p, b''))

        def mock_open_side_effect(filepath, mode='r'):
            if 'b' in mode:
                return io.BytesIO(file_contents.get(filepath, b''))
            return io.StringIO(file_contents.get(filepath, b'').decode())
        mock_open_func.side_effect = mock_open_side_effect

        # Test with min_size = 50 (should ignore small.txt)
        duplicates = find_duplicate_files(['/data'], min_size=50)
        self.assertEqual(duplicates, {})

        # Test with min_size = 5 (should include medium.txt and large.txt, but no duplicates among them)
        duplicates = find_duplicate_files(['/data'], min_size=5)
        self.assertEqual(duplicates, {})

        # Create a duplicate scenario with min_size
        file_contents['/data/medium_copy.txt'] = b'm' * 100
        mock_walk.return_value = [
            ('/data', [], ['small.txt', 'medium.txt', 'large.txt', 'medium_copy.txt']),
        ]
        mock_getsize.side_effect = lambda p: len(file_contents.get(p, b''))

        expected_hash = hashlib.sha256(b'm' * 100).hexdigest()
        duplicates = find_duplicate_files(['/data'], min_size=50)
        self.assertIn(expected_hash, duplicates)
        self.assertCountEqual(duplicates[expected_hash], ['/data/medium.txt', '/data/medium_copy.txt'])

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir', return_value=True)
    def test_find_duplicate_files_empty_files(self, mock_isdir, mock_open_func, mock_getsize, mock_walk):
        # Mock rationale: Ensure the utility correctly handles empty files, which can be duplicates.

        mock_walk.return_value = [
            ('/empty_dir', [], ['empty1.txt', 'empty2.txt']),
        ]

        file_contents = {
            '/empty_dir/empty1.txt': b'',
            '/empty_dir/empty2.txt': b'',
        }
        mock_getsize.side_effect = lambda p: len(file_contents.get(p, b''))

        def mock_open_side_effect(filepath, mode='r'):
            if 'b' in mode:
                return io.BytesIO(file_contents.get(filepath, b''))
            return io.StringIO(file_contents.get(filepath, b'').decode())
        mock_open_func.side_effect = mock_open_side_effect

        expected_hash = hashlib.sha256(b'').hexdigest()
        duplicates = find_duplicate_files(['/empty_dir'])

        self.assertIn(expected_hash, duplicates)
        self.assertCountEqual(duplicates[expected_hash], ['/empty_dir/empty1.txt', '/empty_dir/empty2.txt'])

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('echo_locator.find_duplicate_files')
    @patch('os.path.getsize', return_value=123)
    def test_main_text_output(self, mock_getsize, mock_find_duplicate_files, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Test the `main` function's CLI parsing and output formatting.
        # We mock `argparse` to control input arguments and `find_duplicate_files` to control results.
        # `sys.stdout` is captured to verify the printed output.

        mock_parse_args.return_value = MagicMock(
            directories=['/test_dir'],
            output_format='text',
            min_size=0
        )
        mock_find_duplicate_files.return_value = {
            'hash123': ['/test_dir/fileA.txt', '/test_dir/subdir/fileA_copy.txt'],
            'hash456': ['/test_dir/fileB.txt', '/test_dir/fileB_another.txt']
        }

        main()

        output = mock_stdout.getvalue()
        self.assertIn("Found 2 sets of duplicate files", output)
        self.assertIn("Set 1 (SHA256: hash123):", output)
        self.assertIn("  - /test_dir/fileA.txt", output)
        self.assertIn("  - /test_dir/subdir/fileA_copy.txt", output)
        self.assertIn("Set 2 (SHA256: hash456):", output)
        self.assertIn("  - /test_dir/fileB.txt", output)
        self.assertIn("  - /test_dir/fileB_another.txt", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('echo_locator.find_duplicate_files')
    @patch('os.path.getsize', return_value=123)
    def test_main_json_output(self, mock_getsize, mock_find_duplicate_files, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Similar to `test_main_text_output`, but specifically for JSON output.
        # We verify that the output is valid JSON and contains the expected data structure.

        mock_parse_args.return_value = MagicMock(
            directories=['/test_dir'],
            output_format='json',
            min_size=0
        )
        mock_find_duplicate_files.return_value = {
            'hash123': ['/test_dir/fileA.txt', '/test_dir/subdir/fileA_copy.txt']
        }

        main()

        output = mock_stdout.getvalue()
        try:
            json_output = json.loads(output)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")

        self.assertEqual(len(json_output), 1)
        self.assertEqual(json_output[0]['hash'], 'hash123')
        self.assertEqual(json_output[0]['size'], 123) # From mock_getsize
        self.assertCountEqual(json_output[0]['files'], ['/test_dir/fileA.txt', '/test_dir/subdir/fileA_copy.txt'])

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('echo_locator.find_duplicate_files', return_value={})
    def test_main_no_duplicates_found(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Test the scenario where no duplicates are found.
        # `find_duplicate_files` is mocked to return an empty dictionary.

        mock_parse_args.return_value = MagicMock(
            directories=['/test_dir'],
            output_format='text',
            min_size=0
        )

        main()

        output = mock_stdout.getvalue()
        self.assertIn("No duplicate files found.", output)

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir', side_effect=[True, False]) # First dir exists, second doesn't
    def test_find_duplicate_files_invalid_directory(self, mock_isdir, mock_open_func, mock_getsize, mock_walk):
        # Mock rationale: Test how the utility handles non-existent or inaccessible directories.
        # `os.path.isdir` is mocked to simulate this condition.

        mock_walk.return_value = [
            ('/valid_dir', [], ['file.txt']),
        ]
        file_contents = {'/valid_dir/file.txt': b'content'}
        mock_getsize.side_effect = lambda p: len(file_contents.get(p, b''))
        def mock_open_side_effect(filepath, mode='r'):
            if 'b' in mode:
                return io.BytesIO(file_contents.get(filepath, b''))
            return io.StringIO(file_contents.get(filepath, b'').decode())
        mock_open_func.side_effect = mock_open_side_effect

        # Expect a warning for the invalid directory, but still process the valid one
        duplicates = find_duplicate_files(['/valid_dir', '/invalid_dir'])
        self.assertEqual(duplicates, {})


if __name__ == '__main__':
    unittest.main()
