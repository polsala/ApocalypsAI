import unittest
import os
import hashlib
import sys
from unittest.mock import patch, mock_open

# Import the functions to be tested
from src.manifest_generator import human_readable_size, generate_sha256, generate_manifest, main as manifest_main

class TestManifestGenerator(unittest.TestCase):

    def test_human_readable_size(self):
        self.assertEqual(human_readable_size(0), "0.0 B")
        self.assertEqual(human_readable_size(100), "100.0 B")
        self.assertEqual(human_readable_size(1023), "1023.0 B")
        self.assertEqual(human_readable_size(1024), "1.0 KB")
        self.assertEqual(human_readable_size(1024 * 1024), "1.0 MB")
        self.assertEqual(human_readable_size(1024 * 1024 * 1024), "1.0 GB")
        self.assertEqual(human_readable_size(1024 * 1024 * 1024 * 1024), "1.0 TB")
        self.assertEqual(human_readable_size(1536), "1.5 KB")
        self.assertEqual(human_readable_size(1024 * 1024 * 1.5), "1.5 MB")

    @patch('builtins.open', new_callable=mock_open, read_data=b'test content')
    @patch('os.path.isfile', return_value=True)
    def test_generate_sha256(self, mock_is_file, mock_open_func):
        # Mock rationale: `builtins.open` is mocked to provide predictable file content
        # without actual disk I/O. `os.path.isfile` is mocked to ensure the file is
        # considered existing for the open call.
        expected_hash = hashlib.sha256(b'test content').hexdigest()
        self.assertEqual(generate_sha256("dummy_path.txt"), expected_hash)
        mock_open_func.assert_called_with("dummy_path.txt", "rb")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('os.walk')
    @patch('src.manifest_generator.generate_sha256', return_value='mock_sha256_hash')
    @patch('builtins.print') # Mock print to avoid console output during test
    def test_generate_manifest(self, mock_print, mock_generate_sha256, mock_walk, mock_getsize, mock_isfile, mock_isdir, mock_open_func):
        # Mock rationale:
        # - `os.walk`: To simulate a specific directory structure without creating real files.
        # - `os.path.getsize`: To provide deterministic file sizes for testing size formatting.
        # - `os.path.isfile`: To control which paths are treated as files for size/hash calculation.
        # - `os.path.isdir`: To ensure the root directory is considered valid.
        # - `src.manifest_generator.generate_sha256`: To avoid actual hash calculation and file I/O, providing a fixed hash.
        # - `builtins.open`: To capture the output written to the manifest file without touching the filesystem.
        # - `builtins.print`: To suppress normal output messages during testing.

        # Simulate a directory structure:
        # /root_dir
        # ├── dir_a
        # │   └── file_a.txt (100 bytes)
        # └── file_b.log (2048 bytes)
        mock_walk.return_value = [
            ('/root_dir', ['dir_a'], ['file_b.log']),
            ('/root_dir/dir_a', [], ['file_a.txt'])
        ]

        # Simulate file sizes
        mock_getsize.side_effect = lambda p: {
            '/root_dir/file_b.log': 2048,
            '/root_dir/dir_a/file_a.txt': 100
        }.get(p, 0)

        # Simulate which paths are files
        mock_isfile.side_effect = lambda p: p in [
            '/root_dir/file_b.log',
            '/root_dir/dir_a/file_a.txt'
        ]

        root_dir = '/root_dir'
        output_file = 'test_manifest.md'

        generate_manifest(root_dir, output_file)

        # Get the content written to the mock file
        mock_open_func.assert_called_with(output_file, "w")
        written_content = mock_open_func().write.call_args[0][0]

        expected_content = (
            "# Scavenger Manifest for /root_dir\n"
            "| Type | Path | Size | SHA256 Hash |\n"
            "|---|---|---|---|\n"
            "| Directory | /root_dir/dir_a | - | - |\n"
            "| File | /root_dir/dir_a/file_a.txt | 100.0 B | mock_sha256_hash |\n"
            "| File | /root_dir/file_b.log | 2.0 KB | mock_sha256_hash |"
        )
        
        # Split and compare lines to avoid issues with trailing newlines or slight formatting differences
        expected_lines = [line.strip() for line in expected_content.split('\n') if line.strip()]
        actual_lines = [line.strip() for line in written_content.split('\n') if line.strip()]

        self.assertEqual(actual_lines, expected_lines)
        mock_print.assert_called_with(f"Manifest successfully generated at {output_file}")


    @patch('builtins.print')
    @patch('os.path.isdir', return_value=False)
    @patch('sys.argv', ['manifest_generator.py', '--path', '/nonexistent', '--output', 'output.md'])
    def test_main_invalid_path(self, mock_isdir, mock_print):
        # Mock rationale: `os.path.isdir` is mocked to simulate an invalid input path.
        # `sys.argv` is mocked to simulate command-line arguments.
        # `builtins.print` is mocked to capture output messages.
        # `sys.exit` is caught by `assertRaises(SystemExit)`.
        
        with self.assertRaises(SystemExit) as cm:
            manifest_main()

        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_called_with("Error: The provided path '/nonexistent' is not a valid directory.")

    @patch('builtins.print')
    @patch('os.path.isdir', return_value=True)
    @patch('sys.argv', ['manifest_generator.py', '--path', '/validpath', '--output', 'output.md'])
    @patch('src.manifest_generator.generate_manifest', return_value=0) # Simulate successful manifest generation
    def test_main_valid_path_success(self, mock_generate_manifest, mock_isdir, mock_print):
        # Mock rationale: `os.path.isdir` is mocked to simulate a valid input path.
        # `sys.argv` is mocked to simulate command-line arguments.
        # `src.manifest_generator.generate_manifest` is mocked to simulate the core logic's success.
        # `builtins.print` is mocked to capture output messages (though generate_manifest handles its own).
        
        with self.assertRaises(SystemExit) as cm:
            manifest_main()
        
        self.assertEqual(cm.exception.code, 0)
        mock_generate_manifest.assert_called_once_with('/validpath', 'output.md')
        mock_print.assert_not_called() # generate_manifest handles its own printing for success, not main.

    @patch('builtins.print')
    @patch('os.path.isdir', return_value=True)
    @patch('sys.argv', ['manifest_generator.py', '--path', '/validpath', '--output', 'output.md'])
    @patch('src.manifest_generator.generate_manifest', return_value=1) # Simulate failed manifest generation
    def test_main_valid_path_failure(self, mock_generate_manifest, mock_isdir, mock_print):
        # Mock rationale: Similar to success case, but `generate_manifest` returns 1 to simulate failure.
        
        with self.assertRaises(SystemExit) as cm:
            manifest_main()
        
        self.assertEqual(cm.exception.code, 1)
        mock_generate_manifest.assert_called_once_with('/validpath', 'output.md')
        mock_print.assert_not_called() # generate_manifest handles its own printing for failure, not main.
