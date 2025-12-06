import unittest
from unittest.mock import patch, MagicMock
import os
import datetime # This datetime is the real one, used for creating fixed_now objects
import zipfile # Import real zipfile for ZIP_DEFLATED constant

# Mock rationale:
# os.path.exists: To simulate the existence or non-existence of source/output directories without touching the filesystem.
# os.path.isdir: To simulate if a path is a directory without touching the filesystem.
# os.makedirs: To prevent actual directory creation during tests.
# os.walk: To simulate files within a directory structure without creating actual files.
# zipfile.ZipFile: To prevent actual zip file creation and verify that the 'write' method was called with the expected arguments.
# src.time_capsule.datetime: To ensure the timestamp in the filename is predictable for testing by controlling datetime.datetime.now().

class TestTimeCapsule(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.makedirs')
    @patch('os.walk')
    @patch('zipfile.ZipFile')
    @patch('src.time_capsule.datetime') # Patch the datetime module used by time_capsule.py
    def test_create_capsule_success(self, mock_datetime_module, mock_zipfile, mock_os_walk, mock_makedirs, mock_os_isdir, mock_os_path_exists):
        from src.time_capsule import create_capsule

        # Mock setup
        mock_os_path_exists.side_effect = lambda path: path in ['/mock/source', '/mock/output']
        mock_os_isdir.side_effect = lambda path: path == '/mock/source'
        mock_os_walk.return_value = [
            ('/mock/source', [], ['file1.txt', 'file2.jpg']),
            ('/mock/source/subdir', [], ['subfile.log'])
        ]
        
        # Mock datetime.datetime.now() to return a fixed time
        fixed_now = datetime.datetime(2023, 10, 27, 14, 30, 0)
        mock_datetime_module.datetime.now.return_value = fixed_now
        
        mock_zip_instance = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

        source_dir = '/mock/source'
        output_dir = '/mock/output'
        prefix = 'test_capsule'
        expected_capsule_filename = f"{prefix}_{fixed_now.strftime('%Y%m%d_%H%M%S')}.zip"
        expected_capsule_path = os.path.join(output_dir, expected_capsule_filename)

        result = create_capsule(source_dir, output_dir, prefix)

        mock_os_path_exists.assert_any_call(source_dir)
        mock_os_isdir.assert_called_once_with(source_dir)
        mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)
        mock_zipfile.assert_called_once_with(expected_capsule_path, 'w', zipfile.ZIP_DEFLATED)
        
        # Verify write calls
        mock_zip_instance.write.assert_any_call('/mock/source/file1.txt', 'file1.txt')
        mock_zip_instance.write.assert_any_call('/mock/source/file2.jpg', 'file2.jpg')
        mock_zip_instance.write.assert_any_call('/mock/source/subdir/subfile.log', os.path.join('subdir', 'subfile.log'))
        self.assertEqual(mock_zip_instance.write.call_count, 3)
        self.assertEqual(result, expected_capsule_path)

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.makedirs')
    @patch('zipfile.ZipFile')
    def test_create_capsule_source_dir_not_exists(self, mock_zipfile, mock_makedirs, mock_os_isdir, mock_os_path_exists):
        from src.time_capsule import create_capsule

        mock_os_path_exists.return_value = False # Source dir does not exist
        mock_os_isdir.return_value = False # Not relevant if path doesn't exist

        result = create_capsule('/nonexistent/source', '/mock/output')

        mock_os_path_exists.assert_called_once_with('/nonexistent/source')
        mock_makedirs.assert_not_called()
        mock_zipfile.assert_not_called()
        self.assertEqual(result, "")

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.makedirs')
    @patch('zipfile.ZipFile')
    def test_create_capsule_source_is_not_directory(self, mock_zipfile, mock_makedirs, mock_os_isdir, mock_os_path_exists):
        from src.time_capsule import create_capsule

        mock_os_path_exists.return_value = True # Path exists
        mock_os_isdir.return_value = False # But it's not a directory

        result = create_capsule('/mock/file.txt', '/mock/output')

        mock_os_path_exists.assert_called_once_with('/mock/file.txt')
        mock_os_isdir.assert_called_once_with('/mock/file.txt')
        mock_makedirs.assert_not_called()
        mock_zipfile.assert_not_called()
        self.assertEqual(result, "")

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.makedirs')
    @patch('os.walk')
    @patch('zipfile.ZipFile')
    @patch('src.time_capsule.datetime') # Patch the datetime module used by time_capsule.py
    def test_create_capsule_empty_source_dir(self, mock_datetime_module, mock_zipfile, mock_os_walk, mock_makedirs, mock_os_isdir, mock_os_path_exists):
        from src.time_capsule import create_capsule

        mock_os_path_exists.side_effect = lambda path: path in ['/mock/empty_source', '/mock/output']
        mock_os_isdir.side_effect = lambda path: path == '/mock/empty_source'
        mock_os_walk.return_value = [('/mock/empty_source', [], [])] # Empty directory

        fixed_now = datetime.datetime(2023, 10, 27, 14, 30, 0)
        mock_datetime_module.datetime.now.return_value = fixed_now
        
        mock_zip_instance = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip_instance

        source_dir = '/mock/empty_source'
        output_dir = '/mock/output'
        prefix = 'empty_test'
        expected_capsule_filename = f"{prefix}_{fixed_now.strftime('%Y%m%d_%H%M%S')}.zip"
        expected_capsule_path = os.path.join(output_dir, expected_capsule_filename)

        result = create_capsule(source_dir, output_dir, prefix)

        mock_os_path_exists.assert_any_call(source_dir)
        mock_os_isdir.assert_called_once_with(source_dir)
        mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)
        mock_zipfile.assert_called_once_with(expected_capsule_path, 'w', zipfile.ZIP_DEFLATED)
        mock_zip_instance.write.assert_not_called() # No files to write
        self.assertEqual(result, expected_capsule_path)

    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('os.makedirs')
    @patch('os.walk')
    @patch('zipfile.ZipFile')
    @patch('src.time_capsule.datetime') # Patch the datetime module used by time_capsule.py
    def test_create_capsule_zip_error(self, mock_datetime_module, mock_zipfile, mock_os_walk, mock_makedirs, mock_os_isdir, mock_os_path_exists):
        from src.time_capsule import create_capsule

        mock_os_path_exists.side_effect = lambda path: path in ['/mock/source', '/mock/output']
        mock_os_isdir.side_effect = lambda path: path == '/mock/source'
        mock_os_walk.return_value = [
            ('/mock/source', [], ['file1.txt'])
        ]
        
        fixed_now = datetime.datetime(2023, 10, 27, 14, 30, 0)
        mock_datetime_module.datetime.now.return_value = fixed_now
        
        # Simulate an error during zip file creation
        mock_zipfile.side_effect = Exception("Mock Zip Error")

        source_dir = '/mock/source'
        output_dir = '/mock/output'
        prefix = 'error_test'

        result = create_capsule(source_dir, output_dir, prefix)

        mock_os_path_exists.assert_any_call(source_dir)
        mock_os_isdir.assert_called_once_with(source_dir)
        mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)
        mock_zipfile.assert_called_once() # Called, but raised an exception
        self.assertEqual(result, "")
