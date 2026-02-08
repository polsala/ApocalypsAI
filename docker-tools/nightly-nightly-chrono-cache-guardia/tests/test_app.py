import unittest
import os
import shutil
import tarfile
import time
import datetime
from unittest.mock import patch, mock_open, MagicMock
from cryptography.fernet import Fernet, InvalidToken

# Import the functions to be tested
from app import snapshot_and_encrypt, main

class TestChronoCacheGuardian(unittest.TestCase):

    def setUp(self):
        self.test_source_dir = "/test_source"
        self.test_dest_dir = "/test_dest"
        self.test_encryption_key = Fernet.generate_key()
        self.mock_fernet_instance = Fernet(self.test_encryption_key)

        # Mock rationale: To ensure tests are deterministic and offline, 
        # file system operations (`os.makedirs`, `shutil.copytree`, `tarfile.open`, `open` for file I/O)
        # and time-related functions (`time.sleep`, `datetime.datetime.now`) will be mocked.
        # This prevents actual file system changes and delays during testing.

    @patch('os.path.isdir', return_value=True)
    @patch('os.makedirs')
    @patch('shutil.copytree')
    @patch('tarfile.open')
    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('builtins.open', new_callable=mock_open)
    @patch('datetime.datetime')
    @patch('app.Fernet') # Mock Fernet to control encryption/decryption
    def test_snapshot_and_encrypt_success(self, mock_fernet_class, mock_datetime, mock_open_func, mock_rmtree, mock_remove, mock_tarfile_open, mock_copytree, mock_makedirs, mock_isdir):
        # Mock datetime to return a fixed time
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 30, 0)
        mock_datetime.strftime.return_value = "20231027_103000"

        # Mock Fernet instance and its methods
        mock_fernet_instance = MagicMock()
        mock_fernet_instance.encrypt.return_value = b"encrypted_data_mock"
        mock_fernet_class.return_value = mock_fernet_instance

        # Mock tarfile.open context manager
        mock_tar_file = MagicMock()
        mock_tarfile_open.return_value.__enter__.return_value = mock_tar_file

        # Mock file read/write operations
        mock_open_func.side_effect = [
            mock_open(read_data=b"original_file_data").return_value, # For reading archive_path
            mock_open().return_value # For writing encrypted_file_path
        ]

        result_path = snapshot_and_encrypt(self.test_source_dir, self.test_dest_dir, self.test_encryption_key)

        mock_isdir.assert_called_with(self.test_source_dir)
        mock_makedirs.assert_called_with(self.test_dest_dir, exist_ok=True)
        mock_copytree.assert_called_once()
        mock_tarfile_open.assert_called_once_with(unittest.mock.ANY, "w:gz") # Path will be /tmp/snapshot_temp_...
        mock_tar_file.add.assert_called_once_with(unittest.mock.ANY, arcname=os.path.basename(self.test_source_dir))
        mock_fernet_class.assert_called_once_with(self.test_encryption_key)
        mock_fernet_instance.encrypt.assert_called_once_with(b"original_file_data")
        mock_open_func.assert_any_call(unittest.mock.ANY, "rb") # For reading tar.gz
        mock_open_func.assert_any_call(unittest.mock.ANY, "wb") # For writing encrypted file
        mock_open_func().write.assert_called_with(b"encrypted_data_mock")
        mock_rmtree.assert_called_once()
        mock_remove.assert_called_once()
        self.assertTrue(result_path.endswith(".tar.gz.encrypted"))

    @patch('os.path.isdir', return_value=False)
    def test_snapshot_and_encrypt_source_not_found(self, mock_isdir):
        with self.assertRaises(FileNotFoundError):
            snapshot_and_encrypt(self.test_source_dir, self.test_dest_dir, self.test_encryption_key)
        mock_isdir.assert_called_once_with(self.test_source_dir)

    @patch('os.path.isdir', return_value=True)
    @patch('os.makedirs')
    @patch('shutil.copytree', side_effect=Exception("Copy error"))
    @patch('shutil.rmtree')
    @patch('os.remove')
    def test_snapshot_and_encrypt_copy_error_cleanup(self, mock_remove, mock_rmtree, mock_copytree, mock_makedirs, mock_isdir):
        with self.assertRaises(Exception) as cm:
            snapshot_and_encrypt(self.test_source_dir, self.test_dest_dir, self.test_encryption_key)
        self.assertEqual(str(cm.exception), "Copy error")
        mock_rmtree.assert_called_once() # Ensure cleanup happens even on error
        mock_remove.assert_not_called() # No archive to remove yet

    @patch('os.environ.get', side_effect=lambda k, default=None: {
        "SOURCE_DIR": "/mock_source",
        "DEST_DIR": "/mock_dest",
        "ENCRYPTION_KEY": self.test_encryption_key.decode(),
        "INTERVAL_SECONDS": "1"
    }.get(k, default))
    @patch('app.snapshot_and_encrypt', return_value="/mock_dest/snapshot.tar.gz.encrypted")
    @patch('time.sleep')
    @patch('app.logging')
    def test_main_loop(self, mock_logging, mock_sleep, mock_snapshot_and_encrypt, mock_environ_get):
        # Mock rationale: `time.sleep` is mocked to prevent actual delays during testing.
        # `snapshot_and_encrypt` is mocked to control its behavior and avoid actual file operations.
        # `os.environ.get` is mocked to provide necessary environment variables.
        # `app.logging` is mocked to suppress log output during test and check calls.

        # Simulate running for a short period (e.g., 2 iterations)
        mock_sleep.side_effect = [None, KeyboardInterrupt] # Stop after first sleep

        with self.assertRaises(KeyboardInterrupt):
            main()

        mock_snapshot_and_encrypt.assert_called_once_with(
            "/mock_source", "/mock_dest", self.test_encryption_key
        )
        mock_sleep.assert_called_once_with(1)
        mock_logging.info.assert_any_call(unittest.mock.ANY)

    @patch('os.environ.get', side_effect=lambda k, default=None: {
        "SOURCE_DIR": "/mock_source",
        "DEST_DIR": "/mock_dest",
        "ENCRYPTION_KEY": "invalid_key", # Invalid key
        "INTERVAL_SECONDS": "1"
    }.get(k, default))
    @patch('app.logging')
    @patch('builtins.exit')
    def test_main_invalid_key(self, mock_exit, mock_logging, mock_environ_get):
        main()
        mock_logging.error.assert_called_with(unittest.mock.ANY)
        mock_exit.assert_called_once_with(1)

    @patch('os.environ.get', side_effect=lambda k, default=None: {
        "SOURCE_DIR": None, # Missing
        "DEST_DIR": "/mock_dest",
        "ENCRYPTION_KEY": self.test_encryption_key.decode(),
        "INTERVAL_SECONDS": "1"
    }.get(k, default))
    @patch('app.logging')
    @patch('builtins.exit')
    def test_main_missing_env_vars(self, mock_exit, mock_logging, mock_environ_get):
        main()
        mock_logging.error.assert_called_with("Missing required environment variables: SOURCE_DIR, DEST_DIR, ENCRYPTION_KEY")
        mock_exit.assert_called_once_with(1)

    @patch('os.environ.get', side_effect=lambda k, default=None: {
        "SOURCE_DIR": "/mock_source",
        "DEST_DIR": "/mock_dest",
        "ENCRYPTION_KEY": self.test_encryption_key.decode(),
        "INTERVAL_SECONDS": "1"
    }.get(k, default))
    @patch('app.snapshot_and_encrypt', side_effect=Exception("Snapshot failed"))
    @patch('time.sleep')
    @patch('app.logging')
    def test_main_snapshot_error_continues(self, mock_logging, mock_sleep, mock_snapshot_and_encrypt, mock_environ_get):
        # Simulate running for a short period (e.g., 2 iterations)
        mock_sleep.side_effect = [None, KeyboardInterrupt] # Stop after first sleep

        with self.assertRaises(KeyboardInterrupt):
            main()

        mock_snapshot_and_encrypt.assert_called_once()
        mock_logging.error.assert_called_with("Failed to create snapshot: Snapshot failed")
        mock_sleep.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
