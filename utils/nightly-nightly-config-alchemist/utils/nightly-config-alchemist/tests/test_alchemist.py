import unittest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock
from io import StringIO

# Add the src directory to the path to allow importing alchemist
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import alchemist

class TestAlchemist(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.path.isfile')
    @patch('os.walk')
    def test_find_config_files_directory(self, mock_walk, mock_isfile):
        # Mock rationale: os.walk and os.path.isfile are filesystem operations.
        # We need to control their output to simulate different directory structures
        # and file types without actual disk access.
        mock_isfile.return_value = False # Assume path is a directory
        mock_walk.return_value = [
            ('/root', ['subdir'], ['config.json', 'README.md']),
            ('/root/subdir', [], ['settings.yml', 'data.txt'])
        ]
        extensions = ['.json', '.yml']
        expected_files = [
            os.path.join('/root', 'config.json'),
            os.path.join('/root/subdir', 'settings.yml')
        ]
        self.assertEqual(sorted(alchemist.find_config_files('/root', extensions)), sorted(expected_files))

    @patch('os.path.isfile')
    def test_find_config_files_single_file(self, mock_isfile):
        # Mock rationale: os.path.isfile is a filesystem operation.
        # We need to control its output to simulate a single file path.
        mock_isfile.return_value = True
        extensions = ['.json', '.yml']
        expected_files = ['/root/config.json']
        self.assertEqual(alchemist.find_config_files('/root/config.json', extensions), expected_files)
        self.assertEqual(alchemist.find_config_files('/root/image.png', extensions), []) # Mismatch extension

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext')
    def test_process_file_valid_json_no_change(self, mock_splitext, mock_file_open):
        # Mock rationale: builtins.open simulates file I/O. os.path.splitext simulates file extension check.
        # This allows testing file content and type without actual disk access.
        mock_splitext.return_value = ('test', '.json')
        mock_file_open.return_value.read.return_value = '{
  "key": "value"
}'
        status, msg, original, new = alchemist.process_file('test.json', 2, False)
        self.assertEqual(status, 'ok')
        self.assertIn('already well-formed', msg)
        self.assertEqual(original, '{
  "key": "value"
}')
        self.assertEqual(new, '{
  "key": "value"
}')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext')
    def test_process_file_valid_json_needs_normalization(self, mock_splitext, mock_file_open):
        # Mock rationale: Same as above. Testing normalization logic.
        mock_splitext.return_value = ('test', '.json')
        mock_file_open.return_value.read.return_value = '{"key":"value"}'
        status, msg, original, new = alchemist.process_file('test.json', 2, False)
        self.assertEqual(status, 'needs_normalization')
        self.assertIn('needs normalization', msg)
        self.assertEqual(original, '{"key":"value"}')
        self.assertEqual(new, '{
  "key": "value"
}')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext')
    def test_process_file_valid_json_apply_normalization(self, mock_splitext, mock_file_open):
        # Mock rationale: Same as above. Testing apply mode.
        mock_splitext.return_value = ('test', '.json')
        mock_file_open.return_value.read.return_value = '{"key":"value"}'
        status, msg, original, new = alchemist.process_file('test.json', 2, True)
        self.assertEqual(status, 'normalized')
        self.assertIn('normalized successfully', msg)
        self.assertEqual(original, '{"key":"value"}')
        self.assertEqual(new, '{
  "key": "value"
}')
        mock_file_open.return_value.write.assert_called_once_with('{
  "key": "value"
}')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext')
    def test_process_file_invalid_json(self, mock_splitext, mock_file_open):
        # Mock rationale: Same as above. Testing error handling for invalid JSON.
        mock_splitext.return_value = ('test', '.json')
        mock_file_open.return_value.read.return_value = '{"key":"value"' # Malformed JSON
        status, msg, original, new = alchemist.process_file('test.json', 2, False)
        self.assertEqual(status, 'error')
        self.assertIn('Syntax error', msg)
        self.assertEqual(original, '{"key":"value"')
        self.assertEqual(new, '{"key":"value"') # Content should not change

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext')
    def test_process_file_valid_yaml_no_change(self, mock_splitext, mock_file_open):
        # Mock rationale: Same as above. Testing YAML.
        mock_splitext.return_value = ('test', '.yml')
        mock_file_open.return_value.read.return_value = 'key: value\nlist:\n  - item1\n  - item2\n'
        status, msg, original, new = alchemist.process_file('test.yml', 2, False)
        self.assertEqual(status, 'ok')
        self.assertIn('already well-formed', msg)
        self.assertEqual(original, 'key: value\nlist:\n  - item1\n  - item2\n')
        self.assertEqual(new, 'key: value\nlist:\n  - item1\n  - item2\n')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext')
    def test_process_file_valid_yaml_needs_normalization(self, mock_splitext, mock_file_open):
        # Mock rationale: Same as above. Testing YAML normalization.
        mock_splitext.return_value = ('test', '.yml')
        mock_file_open.return_value.read.return_value = 'key: value\nlist:\n- item1\n- item2\n' # Inconsistent indentation
        status, msg, original, new = alchemist.process_file('test.yml', 2, False)
        self.assertEqual(status, 'needs_normalization')
        self.assertIn('needs normalization', msg)
        self.assertEqual(original, 'key: value\nlist:\n- item1\n- item2\n')
        self.assertEqual(new, 'key: value\nlist:\n  - item1\n  - item2\n') # Should be normalized to 2 spaces

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext')
    def test_process_file_invalid_yaml(self, mock_splitext, mock_file_open):
        # Mock rationale: Same as above. Testing error handling for invalid YAML.
        mock_splitext.return_value = ('test', '.yml')
        mock_file_open.return_value.read.return_value = 'key: - value' # Malformed YAML
        status, msg, original, new = alchemist.process_file('test.yml', 2, False)
        self.assertEqual(status, 'error')
        self.assertIn('Syntax error', msg)
        self.assertEqual(original, 'key: - value')
        self.assertEqual(new, 'key: - value')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext')
    def test_process_file_unsupported_extension(self, mock_splitext, mock_file_open):
        # Mock rationale: Same as above. Testing unsupported file types.
        mock_splitext.return_value = ('test', '.txt')
        mock_file_open.return_value.read.return_value = 'some text'
        status, msg, original, new = alchemist.process_file('test.txt', 2, False)
        self.assertEqual(status, 'skip')
        self.assertIn('Unsupported file type', msg)

    @patch('os.path.exists')
    @patch('alchemist.find_config_files')
    @patch('alchemist.process_file')
    @patch('sys.exit')
    def test_main_success(self, mock_sys_exit, mock_process_file, mock_find_config_files, mock_exists):
        # Mock rationale: os.path.exists, find_config_files, process_file, and sys.exit are
        # external interactions or core logic that needs to be controlled for main function testing.
        mock_exists.return_value = True
        mock_find_config_files.return_value = ['file1.json', 'file2.yml']
        mock_process_file.side_effect = [
            ('ok', 'File is OK.', 'content', 'content'),
            ('ok', 'File is OK.', 'content', 'content')
        ]
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path='.', extensions=['.json', '.yml'], apply=False, indent=2
        )):
            alchemist.main()
            mock_sys_exit.assert_called_once_with(0)
            self.assertIn('Total files processed: 2', sys.stdout.getvalue())
            self.assertIn('Files already OK: 2', sys.stdout.getvalue())

    @patch('os.path.exists')
    @patch('alchemist.find_config_files')
    @patch('alchemist.process_file')
    @patch('sys.exit')
    def test_main_needs_normalization(self, mock_sys_exit, mock_process_file, mock_find_config_files, mock_exists):
        # Mock rationale: Same as above. Testing exit code for 'needs_normalization'.
        mock_exists.return_value = True
        mock_find_config_files.return_value = ['file1.json']
        mock_process_file.return_value = ('needs_normalization', 'Needs normalization.', 'old', 'new')
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path='.', extensions=['.json'], apply=False, indent=2
        )):
            alchemist.main()
            mock_sys_exit.assert_called_once_with(2) # Exit code 2 for no-op (needs changes, but not applied)
            self.assertIn('Files needing normalization (check mode): 1', sys.stdout.getvalue())

    @patch('os.path.exists')
    @patch('alchemist.find_config_files')
    @patch('alchemist.process_file')
    @patch('sys.exit')
    def test_main_error(self, mock_sys_exit, mock_process_file, mock_find_config_files, mock_exists):
        # Mock rationale: Same as above. Testing exit code for errors.
        mock_exists.return_value = True
        mock_find_config_files.return_value = ['file1.json']
        mock_process_file.return_value = ('error', 'Syntax error.', 'old', 'old')
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path='.', extensions=['.json'], apply=False, indent=2
        )):
            alchemist.main()
            mock_sys_exit.assert_called_once_with(1) # Exit code 1 for failure
            self.assertIn('Files with errors: 1', sys.stdout.getvalue())

    @patch('os.path.exists')
    @patch('alchemist.find_config_files')
    @patch('alchemist.process_file')
    @patch('sys.exit')
    def test_main_normalized(self, mock_sys_exit, mock_process_file, mock_find_config_files, mock_exists):
        # Mock rationale: Same as above. Testing exit code for successful normalization.
        mock_exists.return_value = True
        mock_find_config_files.return_value = ['file1.json']
        mock_process_file.return_value = ('normalized', 'Normalized.', 'old', 'new')
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path='.', extensions=['.json'], apply=True, indent=2
        )):
            alchemist.main()
            mock_sys_exit.assert_called_once_with(0) # Exit code 0 for success
            self.assertIn('Files normalized (apply mode): 1', sys.stdout.getvalue())

    @patch('os.path.exists')
    @patch('alchemist.find_config_files')
    @patch('sys.exit')
    def test_main_no_files_found(self, mock_sys_exit, mock_find_config_files, mock_exists):
        # Mock rationale: Same as above. Testing scenario where no files match criteria.
        mock_exists.return_value = True
        mock_find_config_files.return_value = []
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path='.', extensions=['.json'], apply=False, indent=2
        )):
            alchemist.main()
            mock_sys_exit.assert_called_once_with(0) # No-op, not an error
            self.assertIn('No config files found', sys.stdout.getvalue())

    @patch('os.path.exists')
    @patch('sys.exit')
    def test_main_path_not_exists(self, mock_sys_exit, mock_exists):
        # Mock rationale: Same as above. Testing scenario where the provided path doesn't exist.
        mock_exists.return_value = False
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path='/nonexistent', extensions=['.json'], apply=False, indent=2
        )):
            alchemist.main()
            mock_sys_exit.assert_called_once_with(1) # Failure
            self.assertIn('Error: Path \'/nonexistent\' does not exist.', sys.stdout.getvalue())
