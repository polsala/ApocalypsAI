import unittest
import os
import hashlib
from unittest.mock import patch, mock_open, MagicMock
import sys

# Import the functions from the guardian script
from src.guardian import (
    calculate_sha256,
    generate_checksums,
    load_manifest,
    save_manifest,
    verify_checksums,
    main
)

class TestChecksumGuardian(unittest.TestCase):

    def setUp(self):
        # Capture stdout and stderr to prevent test prints from cluttering test runner output
        self.held_stdout = sys.stdout
        self.held_stderr = sys.stderr
        sys.stdout = MagicMock()
        sys.stderr = MagicMock()

    def tearDown(self):
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    def test_calculate_sha256(self):
        # Mock rationale: Avoid actual file system access for deterministic testing.
        # We simulate file content to get a predictable hash.
        mock_file_content = b"test content for hashing"
        expected_hash = hashlib.sha256(mock_file_content).hexdigest()

        with patch('builtins.open', mock_open(read_data=mock_file_content)) as m_open:
            result = calculate_sha256('/fake/path/file.txt')
            self.assertEqual(result, expected_hash)
            m_open.assert_called_once_with('/fake/path/file.txt', 'rb')

    def test_calculate_sha256_file_not_found(self):
        # Mock rationale: Simulate a file not existing to test error handling.
        with patch('builtins.open', side_effect=IOError("No such file")):
            result = calculate_sha256('/nonexistent/file.txt')
            self.assertIsNone(result)
            sys.stderr.assert_called_once_with("Error reading file /nonexistent/file.txt: No such file", file=sys.stderr)

    @patch('os.walk')
    @patch('src.guardian.calculate_sha256')
    def test_generate_checksums(self, mock_calculate_sha256, mock_os_walk):
        # Mock rationale: Simulate a directory structure and file hashes without actual file system operations.
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['file1.txt', 'file2.log']),
            ('/mock/dir/subdir', [], ['subfile.md'])
        ]
        mock_calculate_sha256.side_effect = [
            'hash1',
            'hash2',
            'hash3'
        ]

        expected_checksums = {
            '/mock/dir/file1.txt': 'hash1',
            '/mock/dir/file2.log': 'hash2',
            '/mock/dir/subdir/subfile.md': 'hash3'
        }

        result = generate_checksums('/mock/dir')
        self.assertEqual(result, expected_checksums)
        self.assertEqual(mock_calculate_sha256.call_count, 3)

    def test_load_manifest_existing(self):
        # Mock rationale: Simulate reading an existing manifest file.
        manifest_content = (
            "hashA /path/to/fileA.txt\n"
            "hashB /path/to/fileB.txt\n"
        )
        with patch('builtins.open', mock_open(read_data=manifest_content)) as m_open:
            with patch('os.path.exists', return_value=True):
                result = load_manifest('/fake/manifest.txt')
                expected = {
                    '/path/to/fileA.txt': 'hashA',
                    '/path/to/fileB.txt': 'hashB'
                }
                self.assertEqual(result, expected)
            m_open.assert_called_once_with('/fake/manifest.txt', 'r')

    def test_load_manifest_non_existent(self):
        # Mock rationale: Simulate a manifest file not existing.
        with patch('os.path.exists', return_value=False):
            result = load_manifest('/fake/nonexistent_manifest.txt')
            self.assertEqual(result, {})

    def test_load_manifest_malformed_line(self):
        # Mock rationale: Simulate a manifest file with a malformed line to test robustness.
        manifest_content = (
            "hashA /path/to/fileA.txt\n"
            "malformed_line_without_path\n"
        )
        with patch('builtins.open', mock_open(read_data=manifest_content)) as m_open:
            with patch('os.path.exists', return_value=True):
                result = load_manifest('/fake/manifest.txt')
                expected = {
                    '/path/to/fileA.txt': 'hashA'
                }
                self.assertEqual(result, expected)
                sys.stderr.assert_called_once_with('Warning: Malformed line in manifest: malformed_line_without_path', file=sys.stderr)

    def test_save_manifest(self):
        # Mock rationale: Simulate writing to a manifest file and ensuring directory creation.
        checksums_to_save = {
            '/path/to/fileB.txt': 'hashB',
            '/path/to/fileA.txt': 'hashA'
        }
        expected_content = (
            "hashA /path/to/fileA.txt\n"
            "hashB /path/to/fileB.txt\n"
        )
        m_open = mock_open()
        with patch('builtins.open', m_open):
            with patch('os.makedirs') as mock_makedirs:
                save_manifest('/fake/manifest.txt', checksums_to_save)
                m_open.assert_called_once_with('/fake/manifest.txt', 'w')
                m_open().write.assert_called_once_with(expected_content)
                mock_makedirs.assert_called_once_with('/fake', exist_ok=True)

    @patch('src.guardian.load_manifest')
    @patch('src.guardian.generate_checksums')
    def test_verify_checksums_no_changes(self, mock_generate_checksums, mock_load_manifest):
        # Mock rationale: Simulate a scenario where no files have changed.
        mock_load_manifest.return_value = {
            '/dir/file1.txt': 'hash1',
            '/dir/file2.txt': 'hash2'
        }
        mock_generate_checksums.return_value = {
            '/dir/file1.txt': 'hash1',
            '/dir/file2.txt': 'hash2'
        }

        result = verify_checksums('/mock/dir', '/mock/manifest.txt')
        self.assertTrue(result) # Expect True for no changes
        sys.stdout.assert_any_call('\nNo new files detected.')
        sys.stdout.assert_any_call('\nNo files removed.')
        sys.stdout.assert_any_call('\nNo files modified.')
        sys.stdout.assert_any_call('Files Unchanged: 2')

    @patch('src.guardian.load_manifest')
    @patch('src.guardian.generate_checksums')
    def test_verify_checksums_with_changes(self, mock_generate_checksums, mock_load_manifest):
        # Mock rationale: Simulate files being added, removed, and modified.
        mock_load_manifest.return_value = {
            '/dir/file1.txt': 'hash1_old',
            '/dir/file2.txt': 'hash2',
            '/dir/file_removed.txt': 'hash_removed'
        }
        mock_generate_checksums.return_value = {
            '/dir/file1.txt': 'hash1_new',
            '/dir/file2.txt': 'hash2',
            '/dir/file_added.txt': 'hash_added'
        }

        result = verify_checksums('/mock/dir', '/mock/manifest.txt')
        self.assertFalse(result) # Expect False for changes detected

        sys.stdout.assert_any_call('\nFiles Added:')
        sys.stdout.assert_any_call('  - /dir/file_added.txt')

        sys.stdout.assert_any_call('\nFiles Removed:')
        sys.stdout.assert_any_call('  - /dir/file_removed.txt')

        sys.stdout.assert_any_call('\nFiles Modified:')
        sys.stdout.assert_any_call('  - /dir/file1.txt (Old: hash1_o..., New: hash1_n...)')

        sys.stdout.assert_any_call('Files Unchanged: 1')

    @patch('src.guardian.load_manifest')
    @patch('src.guardian.generate_checksums')
    @patch('src.guardian.save_manifest')
    @patch('os.path.isdir', return_value=True)
    @patch('os.path.exists')
    @patch('argparse.ArgumentParser')
    def test_main_first_run(self, mock_argparse, mock_os_path_exists, mock_os_path_isdir, mock_save_manifest, mock_generate_checksums, mock_load_manifest):
        # Mock rationale: Simulate the first run where a manifest does not exist.
        # We mock argparse to control CLI inputs, os.path.exists to simulate manifest presence,
        # and the core functions to ensure they are called correctly.
        mock_args = MagicMock()
        mock_args.path = '/test/dir'
        mock_args.manifest = '/test/manifest.txt'
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_os_path_exists.side_effect = lambda p: p == '/test/dir' # Only the directory exists, not the manifest
        mock_generate_checksums.return_value = {'/test/dir/file.txt': 'initial_hash'}

        main()

        mock_os_path_exists.assert_any_call('/test/manifest.txt')
        mock_generate_checksums.assert_called_once_with('/test/dir')
        mock_save_manifest.assert_called_once_with('/test/manifest.txt', {'/test/dir/file.txt': 'initial_hash'})
        sys.stdout.assert_any_call("Manifest file '/test/manifest.txt' not found. Generating new manifest...")
        sys.stdout.assert_any_call("Initial manifest generated. Run again to verify.")

    @patch('src.guardian.load_manifest')
    @patch('src.guardian.generate_checksums')
    @patch('src.guardian.save_manifest')
    @patch('os.path.isdir', return_value=True)
    @patch('os.path.exists', return_value=True) # Manifest exists
    @patch('argparse.ArgumentParser')
    @patch('src.guardian.verify_checksums', return_value=True) # No changes detected
    def test_main_subsequent_run_no_changes(self, mock_verify_checksums, mock_argparse, mock_os_path_exists, mock_os_path_isdir, mock_save_manifest, mock_generate_checksums, mock_load_manifest):
        # Mock rationale: Simulate a subsequent run where the manifest exists and no changes are detected.
        mock_args = MagicMock()
        mock_args.path = '/test/dir'
        mock_args.manifest = '/test/manifest.txt'
        mock_argparse.return_value.parse_args.return_value = mock_args

        main()

        mock_os_path_exists.assert_any_call('/test/manifest.txt')
        mock_verify_checksums.assert_called_once_with('/test/dir', '/test/manifest.txt')
        mock_save_manifest.assert_not_called() # Should not save if verifying
        mock_generate_checksums.assert_not_called() # Called by verify_checksums, not directly by main
        sys.stdout.assert_any_call("Manifest file '/test/manifest.txt' found. Verifying integrity...")
        sys.stdout.assert_any_call("All files are intact and unchanged.")

    @patch('src.guardian.load_manifest')
    @patch('src.guardian.generate_checksums')
    @patch('src.guardian.save_manifest')
    @patch('os.path.isdir', return_value=True)
    @patch('os.path.exists', return_value=True) # Manifest exists
    @patch('argparse.ArgumentParser')
    @patch('src.guardian.verify_checksums', return_value=False) # Changes detected
    def test_main_subsequent_run_with_changes(self, mock_verify_checksums, mock_argparse, mock_os_path_exists, mock_os_path_isdir, mock_save_manifest, mock_generate_checksums, mock_load_manifest):
        # Mock rationale: Simulate a subsequent run where the manifest exists and changes are detected.
        mock_args = MagicMock()
        mock_args.path = '/test/dir'
        mock_args.manifest = '/test/manifest.txt'
        mock_argparse.return_value.parse_args.return_value = mock_args

        main()

        mock_os_path_exists.assert_any_call('/test/manifest.txt')
        mock_verify_checksums.assert_called_once_with('/test/dir', '/test/manifest.txt')
        mock_save_manifest.assert_not_called()
        sys.stdout.assert_any_call("Manifest file '/test/manifest.txt' found. Verifying integrity...")
        sys.stdout.assert_any_call("Integrity check completed with detected changes.")

    @patch('os.path.isdir', return_value=False)
    @patch('argparse.ArgumentParser')
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_sys_exit, mock_argparse, mock_os_path_isdir):
        # Mock rationale: Simulate an invalid directory path provided to the CLI.
        mock_args = MagicMock()
        mock_args.path = '/nonexistent/dir'
        mock_args.manifest = '/test/manifest.txt'
        mock_argparse.return_value.parse_args.return_value = mock_args

        main()

        sys.stderr.assert_any_call("Error: Directory '/nonexistent/dir' does not exist or is not a directory.", file=sys.stderr)
        mock_sys_exit.assert_called_once_with(1)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.exists', return_value=False)
    @patch('argparse.ArgumentParser')
    @patch('src.guardian.generate_checksums', return_value={})
    @patch('sys.exit')
    def test_main_first_run_no_files_in_path(self, mock_sys_exit, mock_generate_checksums, mock_argparse, mock_os_path_exists, mock_os_path_isdir):
        # Mock rationale: Simulate a first run where the target directory exists but contains no files.
        mock_args = MagicMock()
        mock_args.path = '/empty/dir'
        mock_args.manifest = '/test/manifest.txt'
        mock_argparse.return_value.parse_args.return_value = mock_args

        main()

        sys.stderr.assert_any_call("No files found in '/empty/dir' to generate a manifest.", file=sys.stderr)
        mock_sys_exit.assert_called_once_with(1)
