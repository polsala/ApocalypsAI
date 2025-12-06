import unittest
import os
import json
import hashlib
from unittest.mock import patch, mock_open
from datetime import datetime

# Mock rationale: We need to test file system operations (reading files, listing directories,
# getting file sizes) without actually touching the disk. This ensures tests are fast,
# deterministic, and don't leave artifacts. `os.walk`, `os.path.getsize`, `open` are mocked.

# Import the functions to be tested
from src.manifest_generator import calculate_sha256, generate_manifest

class TestManifestGenerator(unittest.TestCase):

    def test_calculate_sha256(self):
        # Test with known content and hash
        test_content = b"hello world"
        expected_hash = hashlib.sha256(test_content).hexdigest()
        
        with patch('builtins.open', mock_open(read_data=test_content)) as mock_file:
            hash_result = calculate_sha256("dummy_path.txt")
            self.assertEqual(hash_result, expected_hash)
            mock_file.assert_called_once_with("dummy_path.txt", 'rb')

    def test_calculate_sha256_io_error(self):
        # Test error handling during file read
        with patch('builtins.open', side_effect=IOError("Permission denied")):
            hash_result = calculate_sha256("non_existent.txt")
            self.assertEqual(hash_result, "ERROR")

    @patch('os.path.abspath', return_value='/mock/root')
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('src.manifest_generator.calculate_sha256') # Mock the hash calculation
    def test_generate_manifest_basic(self, mock_calculate_sha256, mock_getsize, mock_walk, mock_isdir, mock_abspath):
        # Mock rationale: `os.walk` is mocked to simulate a directory structure.
        # `os.path.getsize` and `calculate_sha256` are mocked to provide predictable values
        # without actual file system interaction.

        mock_walk.return_value = [
            ('/mock/root', [], ['file1.txt', 'file2.txt']),
            ('/mock/root/subdir', [], ['subfile.log'])
        ]
        mock_getsize.side_effect = [100, 200, 50]
        mock_calculate_sha256.side_effect = [
            'hash1',
            'hash2',
            'hash3'
        ]

        # Freeze timestamp for deterministic output
        mock_now = datetime(2023, 1, 1, 12, 0, 0)
        with patch('src.manifest_generator.datetime') as mock_dt:
            mock_dt.now.return_value = mock_now
            # The actual datetime object's isoformat method will be called.

            manifest = generate_manifest('/mock/root')

            self.assertIn('timestamp', manifest)
            self.assertEqual(manifest['root_path'], '/mock/root')
            self.assertEqual(len(manifest['files']), 3)

            self.assertEqual(manifest['files'][0]['path'], 'file1.txt')
            self.assertEqual(manifest['files'][0]['size'], 100)
            self.assertEqual(manifest['files'][0]['sha256'], 'hash1')

            self.assertEqual(manifest['files'][1]['path'], 'file2.txt')
            self.assertEqual(manifest['files'][1]['size'], 200)
            self.assertEqual(manifest['files'][1]['sha256'], 'hash2')

            self.assertEqual(manifest['files'][2]['path'], os.path.join('subdir', 'subfile.log'))
            self.assertEqual(manifest['files'][2]['size'], 50)
            self.assertEqual(manifest['files'][2]['sha256'], 'hash3')

    @patch('os.path.abspath', return_value='/mock/root')
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.getsize', side_effect=OSError("Permission denied"))
    @patch('src.manifest_generator.calculate_sha256')
    def test_generate_manifest_file_error(self, mock_calculate_sha256, mock_getsize, mock_walk, mock_isdir, mock_abspath):
        # Test error handling for individual files during manifest generation
        mock_walk.return_value = [
            ('/mock/root', [], ['bad_file.txt'])
        ]
        # calculate_sha256 should not be called if getsize fails first
        mock_calculate_sha256.return_value = 'SHOULD_NOT_BE_CALLED'

        mock_now = datetime(2023, 1, 1, 12, 0, 0)
        with patch('src.manifest_generator.datetime') as mock_dt:
            mock_dt.now.return_value = mock_now

            manifest = generate_manifest('/mock/root')

            self.assertEqual(len(manifest['files']), 1)
            self.assertEqual(manifest['files'][0]['path'], 'bad_file.txt')
            self.assertEqual(manifest['files'][0]['size'], -1)
            self.assertEqual(manifest['files'][0]['sha256'], 'ERROR')

    @patch('os.path.abspath', return_value='/mock/non/existent/dir')
    @patch('os.path.isdir', return_value=False)
    def test_generate_manifest_dir_not_found(self, mock_isdir, mock_abspath):
        # Test handling for non-existent root directory
        manifest = generate_manifest('/non/existent/dir')
        self.assertEqual(len(manifest['files']), 0)
        self.assertEqual(manifest['root_path'], '/mock/non/existent/dir')

if __name__ == '__main__':
    unittest.main()
