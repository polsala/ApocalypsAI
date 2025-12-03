import unittest
import os
import json
from unittest.mock import patch, mock_open
from src.manifest_generator import generate_manifest, _human_readable_size

class TestManifestGenerator(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.abspath')
    @patch('os.path.relpath')
    def test_generate_manifest_basic(self, mock_relpath, mock_abspath, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate file system structure and file sizes without actual disk access.
        # This ensures deterministic and offline testing.
        mock_isdir.return_value = True
        mock_abspath.return_value = '/mock/test_dir'
        mock_relpath.side_effect = lambda path, start: path.replace(start + '/', '')

        # Simulate a directory structure
        mock_walk.return_value = [
            ('/mock/test_dir', [], ['file1.txt', 'file2.log']),
            ('/mock/test_dir/subdir', [], ['subfile.json', 'another.txt'])
        ]
        # Simulate file sizes
        mock_getsize.side_effect = {
            '/mock/test_dir/file1.txt': 100,
            '/mock/test_dir/file2.log': 200,
            '/mock/test_dir/subdir/subfile.json': 500,
            '/mock/test_dir/subdir/another.txt': 150,
        }.get

        expected_manifest = {
            "scan_directory": "/mock/test_dir",
            "included_extensions": ["*"],
            "files": [
                {"path": "file1.txt", "size_bytes": 100},
                {"path": "file2.log", "size_bytes": 200},
                {"path": "subdir/subfile.json", "size_bytes": 500},
                {"path": "subdir/another.txt", "size_bytes": 150},
            ],
            "summary": {
                "total_files_scanned": 4,
                "total_size_bytes": 950,
                "total_size_human_readable": "950.00 B"
            }
        }

        manifest = generate_manifest('/mock/test_dir')
        self.assertEqual(manifest, expected_manifest)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.abspath')
    @patch('os.path.relpath')
    def test_generate_manifest_with_extensions(self, mock_relpath, mock_abspath, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate file system structure and file sizes with extension filtering.
        mock_isdir.return_value = True
        mock_abspath.return_value = '/mock/test_dir'
        mock_relpath.side_effect = lambda path, start: path.replace(start + '/', '')

        mock_walk.return_value = [
            ('/mock/test_dir', [], ['file1.txt', 'file2.log', 'image.png']),
            ('/mock/test_dir/subdir', [], ['subfile.json', 'another.txt', 'temp.tmp'])
        ]
        mock_getsize.side_effect = {
            '/mock/test_dir/file1.txt': 100,
            '/mock/test_dir/file2.log': 200,
            '/mock/test_dir/image.png': 300,
            '/mock/test_dir/subdir/subfile.json': 500,
            '/mock/test_dir/subdir/another.txt': 150,
            '/mock/test_dir/subdir/temp.tmp': 50,
        }.get

        extensions = ['.txt', '.json']
        expected_manifest = {
            "scan_directory": "/mock/test_dir",
            "included_extensions": extensions,
            "files": [
                {"path": "file1.txt", "size_bytes": 100},
                {"path": "subdir/subfile.json", "size_bytes": 500},
                {"path": "subdir/another.txt", "size_bytes": 150},
            ],
            "summary": {
                "total_files_scanned": 3,
                "total_size_bytes": 750,
                "total_size_human_readable": "750.00 B"
            }
        }

        manifest = generate_manifest('/mock/test_dir', extensions=extensions)
        self.assertEqual(manifest, expected_manifest)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.abspath')
    @patch('os.path.relpath')
    def test_generate_manifest_empty_directory(self, mock_relpath, mock_abspath, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate an empty directory.
        mock_isdir.return_value = True
        mock_abspath.return_value = '/mock/empty_dir'
        mock_relpath.side_effect = lambda path, start: path.replace(start + '/', '')

        mock_walk.return_value = [
            ('/mock/empty_dir', [], []),
        ]
        mock_getsize.return_value = 0 # Should not be called for empty dir

        expected_manifest = {
            "scan_directory": "/mock/empty_dir",
            "included_extensions": ["*"],
            "files": [],
            "summary": {
                "total_files_scanned": 0,
                "total_size_bytes": 0,
                "total_size_human_readable": "0 B"
            }
        }

        manifest = generate_manifest('/mock/empty_dir')
        self.assertEqual(manifest, expected_manifest)

    @patch('os.path.isdir')
    def test_generate_manifest_directory_not_found(self, mock_isdir):
        # Mock rationale: Simulate a non-existent directory.
        mock_isdir.return_value = False
        with self.assertRaises(FileNotFoundError):
            generate_manifest('/mock/non_existent_dir')

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/mock/test_dir', [], ['file.txt'])])
    @patch('os.path.getsize', side_effect=OSError("Permission denied"))
    @patch('os.path.abspath', return_value='/mock/test_dir')
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start + '/', ''))
    def test_generate_manifest_file_inaccessible(self, mock_relpath, mock_abspath, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file that cannot be accessed (e.g., permission error).
        # The utility should gracefully skip such files.
        expected_manifest = {
            "scan_directory": "/mock/test_dir",
            "included_extensions": ["*"],
            "files": [],
            "summary": {
                "total_files_scanned": 0,
                "total_size_bytes": 0,
                "total_size_human_readable": "0 B"
            }
        }
        manifest = generate_manifest('/mock/test_dir')
        self.assertEqual(manifest, expected_manifest)


    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/mock/test_dir', [], ['file.txt'])])
    @patch('os.path.getsize', return_value=123)
    @patch('os.path.abspath', return_value='/mock/test_dir')
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start + '/', ''))
    def test_generate_manifest_output_file(self, mock_relpath, mock_abspath, mock_getsize, mock_walk, mock_isdir, mock_json_dump, mock_file_open):
        # Mock rationale: Test that the manifest is written to a file when output_file is provided.
        output_path = '/mock/output.json'
        result = generate_manifest('/mock/test_dir', output_file=output_path)
        self.assertIsNone(result) # Should return None when output_file is specified
        mock_file_open.assert_called_once_with(output_path, 'w')
        mock_json_dump.assert_called_once()
        # Verify the content passed to json.dump (simplified check)
        args, kwargs = mock_json_dump.call_args
        self.assertIn("scan_directory", args[0])
        self.assertIn("files", args[0])
        self.assertIn("summary", args[0])

    def test_human_readable_size(self):
        self.assertEqual(_human_readable_size(0), "0 B")
        self.assertEqual(_human_readable_size(100), "100.00 B")
        self.assertEqual(_human_readable_size(1024), "1.00 KB")
        self.assertEqual(_human_readable_size(1536), "1.50 KB")
        self.assertEqual(_human_readable_size(1024 * 1024), "1.00 MB")
        self.assertEqual(_human_readable_size(1024 * 1024 * 1024), "1.00 GB")
        self.assertEqual(_human_readable_size(1024**5), "1.00 PB") # Petabyte
        self.assertEqual(_human_readable_size(1234567890123456789), "1.07 EB") # Exabyte example

if __name__ == '__main__':
    unittest.main()
