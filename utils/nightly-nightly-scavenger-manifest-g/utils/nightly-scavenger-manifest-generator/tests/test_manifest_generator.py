import unittest
import os
import datetime
from unittest.mock import patch, mock_open
from src.manifest_generator import generate_manifest, format_bytes

class TestManifestGenerator(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.relpath')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_manifest_basic(self, mock_file_open, mock_relpath, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence without actual filesystem interaction.
        mock_isdir.return_value = True
        
        # Mock rationale: Simulate directory traversal and file discovery.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log']),
            ('/test_dir/subdir', [], ['subfile.json'])
        ]
        
        # Mock rationale: Provide deterministic file sizes.
        mock_getsize.side_effect = [100, 2048, 5000000] # file1.txt, file2.log, subfile.json
        
        # Mock rationale: Provide deterministic modification times.
        # Using fixed timestamps for deterministic output.
        mock_getmtime.side_effect = [
            datetime.datetime(2023, 1, 1, 10, 0, 0).timestamp(),
            datetime.datetime(2023, 1, 2, 11, 30, 0).timestamp(),
            datetime.datetime(2023, 1, 3, 12, 0, 0).timestamp(),
        ]
        
        # Mock rationale: Simulate relative paths for files within the scanned directory.
        mock_relpath.side_effect = ['file1.txt', 'file2.log', 'subdir/subfile.json']

        output_filename = "test_manifest.md"
        generate_manifest("/test_dir", output_filename)

        mock_file_open.assert_called_once_with(output_filename, 'w', encoding='utf-8')
        written_content = mock_file_open().write.call_args[0][0]

        self.assertIn("# Scavenger's Manifest for 'test_dir'", written_content)
        self.assertIn("| File Path | Size | Last Modified |", written_content)
        self.assertIn("|---|---|---|", written_content)
        self.assertIn("| `file1.txt` | 100.00 B | 2023-01-01T10:00:00 |", written_content)
        self.assertIn("| `file2.log` | 2.00 KB | 2023-01-02T11:30:00 |", written_content)
        self.assertIn("| `subdir/subfile.json` | 4.77 MB | 2023-01-03T12:00:00 |", written_content)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.relpath')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_manifest_with_extensions(self, mock_file_open, mock_relpath, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence.
        mock_isdir.return_value = True
        
        # Mock rationale: Simulate directory traversal with various file types.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log', 'image.png']),
            ('/test_dir/subdir', [], ['subfile.json', 'temp.tmp'])
        ]
        
        # Mock rationale: Provide deterministic file sizes.
        mock_getsize.side_effect = [100, 2048, 5000000] # file1.txt, file2.log, subfile.json (only these will be processed)
        
        # Mock rationale: Provide deterministic modification times.
        mock_getmtime.side_effect = [
            datetime.datetime(2023, 1, 1, 10, 0, 0).timestamp(),
            datetime.datetime(2023, 1, 2, 11, 30, 0).timestamp(),
            datetime.datetime(2023, 1, 3, 12, 0, 0).timestamp(),
        ]
        
        # Mock rationale: Simulate relative paths.
        mock_relpath.side_effect = ['file1.txt', 'file2.log', 'subdir/subfile.json']

        output_filename = "test_manifest.md"
        generate_manifest("/test_dir", output_filename, file_extensions=['.txt', '.json'])

        mock_file_open.assert_called_once_with(output_filename, 'w', encoding='utf-8')
        written_content = mock_file_open().write.call_args[0][0]

        self.assertIn("| `file1.txt` | 100.00 B | 2023-01-01T10:00:00 |", written_content)
        self.assertIn("| `subdir/subfile.json` | 4.77 MB | 2023-01-03T12:00:00 |", written_content)
        self.assertNotIn("file2.log", written_content) # Should be filtered out
        self.assertNotIn("image.png", written_content) # Should be filtered out
        self.assertNotIn("temp.tmp", written_content) # Should be filtered out

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_manifest_empty_directory(self, mock_file_open, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence.
        mock_isdir.return_value = True
        
        # Mock rationale: Simulate an empty directory.
        mock_walk.return_value = [
            ('/empty_dir', [], [])
        ]

        output_filename = "empty_manifest.md"
        generate_manifest("/empty_dir", output_filename)

        mock_file_open.assert_called_once_with(output_filename, 'w', encoding='utf-8')
        written_content = mock_file_open().write.call_args[0][0]

        self.assertIn("# Scavenger's Manifest for 'empty_dir'", written_content)
        self.assertIn("| File Path | Size | Last Modified |", written_content)
        self.assertIn("|---|---|---|", written_content)
        self.assertEqual(written_content.count('|'), 6) # Header + separator lines

    @patch('os.path.isdir')
    def test_generate_manifest_invalid_directory(self, mock_isdir):
        # Mock rationale: Simulate a non-existent directory.
        mock_isdir.return_value = False
        
        with self.assertRaisesRegex(ValueError, "Directory not found: /non_existent_dir"):
            generate_manifest("/non_existent_dir", "output.md")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    @patch('os.path.relpath')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_manifest_os_error_on_file(self, mock_file_open, mock_relpath, mock_getmtime, mock_getsize, mock_walk, mock_isdir):
        # Mock rationale: Simulate directory existence.
        mock_isdir.return_value = True
        
        # Mock rationale: Simulate directory traversal with one problematic file.
        mock_walk.return_value = [
            ('/test_dir', [], ['good_file.txt', 'bad_file.txt'])
        ]
        
        # Mock rationale: Simulate a good file and then an OSError for the bad file.
        mock_getsize.side_effect = [
            100,
            OSError("Permission denied")
        ]
        
        # Mock rationale: Provide deterministic modification times for the good file.
        mock_getmtime.side_effect = [
            datetime.datetime(2023, 1, 1, 10, 0, 0).timestamp()
        ]
        
        # Mock rationale: Simulate relative paths.
        mock_relpath.side_effect = ['good_file.txt', 'bad_file.txt']

        output_filename = "error_manifest.md"
        generate_manifest("/test_dir", output_filename)

        mock_file_open.assert_called_once_with(output_filename, 'w', encoding='utf-8')
        written_content = mock_file_open().write.call_args[0][0]

        self.assertIn("| `good_file.txt` | 100.00 B | 2023-01-01T10:00:00 |", written_content)
        self.assertIn("| `bad_file.txt` | ERROR: Permission denied | ERROR |", written_content)

    def test_format_bytes(self):
        self.assertEqual(format_bytes(0), "0.00 B")
        self.assertEqual(format_bytes(100), "100.00 B")
        self.assertEqual(format_bytes(1023), "1023.00 B")
        self.assertEqual(format_bytes(1024), "1.00 KB")
        self.assertEqual(format_bytes(1536), "1.50 KB")
        self.assertEqual(format_bytes(1024**2), "1.00 MB")
        self.assertEqual(format_bytes(1024**3), "1.00 GB")
        self.assertEqual(format_bytes(1024**4), "1.00 TB")
        self.assertEqual(format_bytes(1024**5), "1.00 PB") # Beyond TB, it should still format.
        self.assertEqual(format_bytes(1024**6), "1024.00 PB") # Just to check the limit

if __name__ == '__main__':
    unittest.main()
