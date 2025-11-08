import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import subprocess

# Add the src directory to the path to allow importing cleaner.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import cleaner

class TestCosmicCacheCleaner(unittest.TestCase):

    @patch('shutil.which')
    @patch('subprocess.run')
    def test_clear_all_caches_when_all_tools_exist(self, mock_subprocess_run, mock_shutil_which):
        # Mock rationale: Simulate all necessary commands existing in PATH.
        mock_shutil_which.side_effect = lambda cmd: '/usr/bin/' + cmd if cmd in ['pip', 'npm', 'yarn', 'go'] else None
        
        # Mock rationale: Simulate successful execution for all cache clearing commands.
        mock_subprocess_run.return_value = MagicMock(stdout='Cache cleared successfully', stderr='', returncode=0)

        cleaner.main()

        # Assert that shutil.which was called for each expected command
        mock_shutil_which.assert_any_call('pip')
        mock_shutil_which.assert_any_call('npm')
        mock_shutil_which.assert_any_call('yarn')
        mock_shutil_which.assert_any_call('go')

        # Assert that subprocess.run was called with the correct commands
        mock_subprocess_run.assert_any_call(['pip', 'cache', 'purge'], check=True, capture_output=True, text=True)
        mock_subprocess_run.assert_any_call(['npm', 'cache', 'clean', '--force'], check=True, capture_output=True, text=True)
        mock_subprocess_run.assert_any_call(['yarn', 'cache', 'clean'], check=True, capture_output=True, text=True)
        mock_subprocess_run.assert_any_call(['go', 'clean', '-modcache'], check=True, capture_output=True, text=True)
        
        # Ensure it was called exactly 4 times for the 4 cache types
        self.assertEqual(mock_subprocess_run.call_count, 4)

    @patch('shutil.which')
    @patch('subprocess.run')
    def test_skip_caches_when_tools_do_not_exist(self, mock_subprocess_run, mock_shutil_which):
        # Mock rationale: Simulate only 'pip' and 'go' existing in PATH, 'npm' and 'yarn' not.
        mock_shutil_which.side_effect = lambda cmd: '/usr/bin/' + cmd if cmd in ['pip', 'go'] else None
        
        # Mock rationale: Simulate successful execution for the existing tools.
        mock_subprocess_run.return_value = MagicMock(stdout='Cache cleared successfully', stderr='', returncode=0)

        cleaner.main()

        # Assert that shutil.which was called for each expected command
        mock_shutil_which.assert_any_call('pip')
        mock_shutil_which.assert_any_call('npm') # Still checks, but returns None
        mock_shutil_which.assert_any_call('yarn') # Still checks, but returns None
        mock_shutil_which.assert_any_call('go')

        # Assert that subprocess.run was only called for pip and go
        mock_subprocess_run.assert_any_call(['pip', 'cache', 'purge'], check=True, capture_output=True, text=True)
        mock_subprocess_run.assert_any_call(['go', 'clean', '-modcache'], check=True, capture_output=True, text=True)
        
        # Ensure it was called exactly 2 times
        self.assertEqual(mock_subprocess_run.call_count, 2)

    @patch('shutil.which')
    @patch('subprocess.run')
    def test_handle_command_execution_failure(self, mock_subprocess_run, mock_shutil_which):
        # Mock rationale: Simulate all commands existing, but 'npm' failing to execute with a non-zero exit code.
        mock_shutil_which.side_effect = lambda cmd: '/usr/bin/' + cmd if cmd in ['pip', 'npm', 'yarn', 'go'] else None
        
        # Mock rationale: Configure subprocess.run to raise CalledProcessError for npm, succeed for others.
        def run_side_effect(command, **kwargs):
            if command[0] == 'npm':
                raise subprocess.CalledProcessError(1, command, stdout='some output', stderr='npm error')
            return MagicMock(stdout='Cache cleared successfully', stderr='', returncode=0)

        mock_subprocess_run.side_effect = run_side_effect

        cleaner.main()

        # Assert that all checks were made
        mock_shutil_which.assert_any_call('pip')
        mock_shutil_which.assert_any_call('npm')
        mock_shutil_which.assert_any_call('yarn')
        mock_shutil_which.assert_any_call('go')

        # Assert that subprocess.run was called for all, and npm's call raised CalledProcessError
        mock_subprocess_run.assert_any_call(['pip', 'cache', 'purge'], check=True, capture_output=True, text=True)
        mock_subprocess_run.assert_any_call(['npm', 'cache', 'clean', '--force'], check=True, capture_output=True, text=True)
        mock_subprocess_run.assert_any_call(['yarn', 'cache', 'clean'], check=True, capture_output=True, text=True)
        mock_subprocess_run.assert_any_call(['go', 'clean', '-modcache'], check=True, capture_output=True, text=True)
        
        self.assertEqual(mock_subprocess_run.call_count, 4)

    @patch('shutil.which')
    @patch('subprocess.run')
    def test_handle_command_not_found_during_execution(self, mock_subprocess_run, mock_shutil_which):
        # Mock rationale: Simulate all commands existing in PATH according to shutil.which.
        mock_shutil_which.side_effect = lambda cmd: '/usr/bin/' + cmd if cmd in ['pip', 'npm', 'yarn', 'go'] else None
        
        # Mock rationale: Configure subprocess.run to raise FileNotFoundError for 'npm' during execution.
        def run_side_effect(command, **kwargs):
            if command[0] == 'npm':
                raise FileNotFoundError(f"No such file or directory: '{command[0]}'")
            return MagicMock(stdout='Cache cleared successfully', stderr='', returncode=0)

        mock_subprocess_run.side_effect = run_side_effect

        cleaner.main()

        # Assert that all checks were made
        mock_shutil_which.assert_any_call('pip')
        mock_shutil_which.assert_any_call('npm')
        mock_shutil_which.assert_any_call('yarn')
        mock_shutil_which.assert_any_call('go')

        # Assert that subprocess.run was called for all, and npm's call raised FileNotFoundError
        mock_subprocess_run.assert_any_call(['pip', 'cache', 'purge'], check=True, capture_output=True, text=True)
        mock_subprocess_run.assert_any_call(['npm', 'cache', 'clean', '--force'], check=True, capture_output=True, text=True)
        mock_subprocess_run.assert_any_call(['yarn', 'cache', 'clean'], check=True, capture_output=True, text=True)
        mock_subprocess_run.assert_any_call(['go', 'clean', '-modcache'], check=True, capture_output=True, text=True)
        
        self.assertEqual(mock_subprocess_run.call_count, 4)


if __name__ == '__main__':
    unittest.main()
