import unittest
import os
import sys
from unittest.mock import patch, mock_open
from src.checker import ConfigChaosChecker
import argparse

class TestConfigChaosChecker(unittest.TestCase):

    def setUp(self):
        self.checker = ConfigChaosChecker()

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_sensitive_data_detection_env(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a file system with a .env file containing sensitive data.
        # mock_os_walk allows control over directory structure.
        # mock_file_open allows control over file content without actual disk I/O.
        mock_os_walk.return_value = [
            ('/app', [], ['.env'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data='API_KEY=supersecretkey123\nDB_PASSWORD=mypassword\nUSER=test').return_value,
        ]

        self.checker.scan_directory('/app')
        issues = self.checker.issues

        self.assertEqual(len(issues), 2)
        self.assertIn(('/app/.env', 'CRITICAL', "Sensitive data detected for 'API_KEY'. Consider using environment variables or a secret management system."), issues)
        self.assertIn(('/app/.env', 'CRITICAL', "Sensitive data detected for 'DB_PASSWORD'. Consider using environment variables or a secret management system."), issues)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_sensitive_data_detection_ini(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a file system with an .ini file containing sensitive data.
        mock_os_walk.return_value = [
            ('/app', [], ['config.ini'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data='[database]\nhost=localhost\nport=5432\ndb_password=insecurepass\n[api]\napi_token=anothersecret').return_value,
        ]

        self.checker.scan_directory('/app')
        issues = self.checker.issues

        self.assertEqual(len(issues), 2)
        self.assertIn(('/app/config.ini', 'CRITICAL', "Sensitive data detected for 'database.db_password'. Consider using environment variables or a secret management system."), issues)
        self.assertIn(('/app/config.ini', 'CRITICAL', "Sensitive data detected for 'api.api_token'. Consider using environment variables or a secret management system."), issues)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_empty_value_detection_env(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a .env file with an empty critical value.
        mock_os_walk.return_value = [
            ('/app', [], ['.env'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data='DATABASE_URL=\nHOST=localhost\nAPP_ENV=').return_value,
        ]

        self.checker.scan_directory('/app')
        issues = self.checker.issues

        self.assertEqual(len(issues), 2)
        self.assertIn(('/app/.env', 'WARNING', "Empty value for 'DATABASE_URL'. This might cause unexpected behavior."), issues)
        self.assertIn(('/app/.env', 'WARNING', "Empty value for 'APP_ENV'. This might cause unexpected behavior."), issues)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_empty_value_detection_ini(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate an .ini file with an empty critical value.
        mock_os_walk.return_value = [
            ('/app', [], ['config.ini'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data='[database]\nhost=localhost\ndb_name=\n[app]\napp_env=').return_value,
        ]

        self.checker.scan_directory('/app')
        issues = self.checker.issues

        self.assertEqual(len(issues), 2)
        self.assertIn(('/app/config.ini', 'WARNING', "Empty value for 'database.db_name'. This might cause unexpected behavior."), issues)
        self.assertIn(('/app/config.ini', 'WARNING', "Empty value for 'app.app_env'. This might cause unexpected behavior."), issues)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_duplicate_key_detection_env(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a .env file with a duplicate key.
        mock_os_walk.return_value = [
            ('/app', [], ['.env'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data='DEBUG=true\nHOST=localhost\nDEBUG=false').return_value,
        ]

        self.checker.scan_directory('/app')
        issues = self.checker.issues

        self.assertEqual(len(issues), 1)
        self.assertIn(('/app/.env', 'WARNING', "Duplicate key 'DEBUG' found. The last definition will likely be used, but this indicates a potential error."), issues)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_duplicate_key_detection_ini(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate an .ini file with a duplicate key within a section.
        mock_os_walk.return_value = [
            ('/app', [], ['config.ini'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data='[app]\ndebug_mode=true\nhost=127.0.0.1\ndebug_mode=false').return_value,
        ]

        self.checker.scan_directory('/app')
        issues = self.checker.issues

        self.assertEqual(len(issues), 1)
        self.assertIn(('/app/config.ini', 'WARNING', "Duplicate key 'debug_mode' found. The last definition will likely be used, but this indicates a potential error."), issues)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_no_issues(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a clean directory with no config issues.
        mock_os_walk.return_value = [
            ('/app', [], ['.env', 'config.ini'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data='APP_NAME=MyApp\nENV=production').return_value,
            mock_open(read_data='[database]\nhost=localhost\nport=5432').return_value,
        ]

        self.checker.scan_directory('/app')
        issues = self.checker.issues

        self.assertEqual(len(issues), 0)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_files_and_directories(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a more complex file system with multiple files and directories.
        mock_os_walk.return_value = [
            ('/app', ['subdir'], ['.env']),
            ('/app/subdir', [], ['config.ini'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data='API_KEY=secret\nUSER=admin').return_value, # /app/.env
            mock_open(read_data='[db]\ndb_password=pass\n[app]\napp_env=').return_value, # /app/subdir/config.ini
        ]

        self.checker.scan_directory('/app')
        issues = self.checker.issues

        self.assertEqual(len(issues), 3)
        self.assertIn(('/app/.env', 'CRITICAL', "Sensitive data detected for 'API_KEY'. Consider using environment variables or a secret management system."), issues)
        self.assertIn(('/app/subdir/config.ini', 'CRITICAL', "Sensitive data detected for 'db.db_password'. Consider using environment variables or a secret management system."), issues)
        self.assertIn(('/app/subdir/config.ini', 'WARNING', "Empty value for 'app.app_env'. This might cause unexpected behavior."), issues)

    @patch('os.path.isdir', return_value=False)
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_invalid_path(self, mock_print, mock_exit, mock_isdir):
        # Mock rationale: Test the main function's error handling for an invalid path.
        # mock_isdir controls the path validation.
        # mock_exit and mock_print capture the program's output and exit behavior.
        from src.checker import main # Import here to get the patched version
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(path='/nonexistent')):
            main()
            mock_print.assert_called_with("Error: Directory not found at '/nonexistent'")
            mock_exit.assert_called_with(1)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_report_no_issues_message(self, mock_print, mock_file_open, mock_os_walk):
        # Mock rationale: Verify the 'no chaos detected' message is printed when no issues are found.
        mock_os_walk.return_value = [
            ('/app', [], ['.env'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data='APP_NAME=MyApp').return_value,
        ]

        self.checker.scan_directory('/app')
        mock_print.assert_any_call('\nNo chaos detected. Your configurations are in pristine order!')

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_report_issues_message(self, mock_print, mock_file_open, mock_os_walk):
        # Mock rationale: Verify the issue report format when issues are found.
        mock_os_walk.return_value = [
            ('/app', [], ['.env'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data='API_KEY=secret').return_value,
        ]

        self.checker.scan_directory('/app')
        mock_print.assert_any_call('\n--- Chaos Report ---')
        mock_print.assert_any_call("File: /app/.env")
        mock_print.assert_any_call("  [CRITICAL] Sensitive data detected for 'API_KEY'. Consider using environment variables or a secret management system.")
        mock_print.assert_any_call('\n--- Scan Complete ---')

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_duplicate_key_across_ini_sections(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate an .ini file with a key duplicated across different sections.
        # The checker should report this as a potential 'chaos point' even if configparser handles it.
        mock_os_walk.return_value = [
            ('/app', [], ['multi_section.ini'])
        ]
        mock_file_open.side_effect = [
            mock_open(read_data='[section1]\ncommon_key=value1\n[section2]\ncommon_key=value2').return_value,
        ]

        self.checker.scan_directory('/app')
        issues = self.checker.issues

        self.assertEqual(len(issues), 1)
        self.assertIn(('/app/multi_section.ini', 'WARNING', "Duplicate key 'common_key' found. The last definition will likely be used, but this indicates a potential error."), issues)
