import unittest
from unittest.mock import patch, MagicMock
import datetime
import subprocess
import sys
import os

# Add the src directory to the path to allow importing vital_signs
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import vital_signs

class TestVitalSigns(unittest.TestCase):

    @patch('subprocess.run')
    @patch('datetime.datetime')
    def test_get_commit_count_success(self, mock_datetime, mock_subprocess_run):
        # Mock rationale: Simulate current time for deterministic 'since' date calculation.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.timedelta = datetime.timedelta # Keep original timedelta

        # Mock rationale: Simulate git log output for 5 commits.
        mock_subprocess_run.return_value = MagicMock(
            stdout='abc\ndef\nghi\njkl\nmno',
            stderr='',
            returncode=0
        )
        self.assertEqual(vital_signs.get_commit_count(7), 5)

        # Test with 0 commits
        # Mock rationale: Simulate git log output for 0 commits (empty string).
        mock_subprocess_run.return_value = MagicMock(
            stdout='',
            stderr='',
            returncode=0
        )
        self.assertEqual(vital_signs.get_commit_count(7), 0)

        # Test with a single commit
        # Mock rationale: Simulate git log output for 1 commit.
        mock_subprocess_run.return_value = MagicMock(
            stdout='abc',
            stderr='',
            returncode=0
        )
        self.assertEqual(vital_signs.get_commit_count(7), 1)

    @patch('subprocess.run')
    @patch('datetime.datetime')
    def test_get_commit_count_git_error(self, mock_datetime, mock_subprocess_run):
        # Mock rationale: Simulate current time for deterministic 'since' date calculation.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.timedelta = datetime.timedelta # Keep original timedelta

        # Mock rationale: Simulate a CalledProcessError from git command.
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(
            returncode=128, cmd=['git', 'log'], stderr='fatal: not a git repository'
        )
        # Redirect stderr to capture output for assertion
        with patch('sys.stderr', new_callable=MagicMock) as mock_stderr:
            self.assertEqual(vital_signs.get_commit_count(7), -1)
            mock_stderr.write.assert_any_call("Error running git command: Command '['git', 'log']' returned non-zero exit status 128.\n")
            mock_stderr.write.assert_any_call("Stderr: fatal: not a git repository\n")

    @patch('subprocess.run')
    @patch('datetime.datetime')
    def test_get_commit_count_git_not_found(self, mock_datetime, mock_subprocess_run):
        # Mock rationale: Simulate current time for deterministic 'since' date calculation.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.timedelta = datetime.timedelta # Keep original timedelta

        # Mock rationale: Simulate FileNotFoundError if 'git' command is not found.
        mock_subprocess_run.side_effect = FileNotFoundError()
        # Redirect stderr to capture output for assertion
        with patch('sys.stderr', new_callable=MagicMock) as mock_stderr:
            self.assertEqual(vital_signs.get_commit_count(7), -1)
            mock_stderr.write.assert_any_call("Error: 'git' command not found. Is Git installed and in your PATH?\n")

    def test_get_heartbeat_diagnosis(self):
        self.assertEqual(vital_signs.get_heartbeat_diagnosis(-1), "Unable to take pulse. Repository might be in a coma or Git is not installed.")
        self.assertEqual(vital_signs.get_heartbeat_diagnosis(0), "The repository seems to be in a deep slumber. Perhaps a jolt of inspiration is needed?")
        self.assertEqual(vital_signs.get_heartbeat_diagnosis(0.5), "A faint pulse detected. The repository is resting, but showing signs of life.")
        self.assertEqual(vital_signs.get_heartbeat_diagnosis(2.0), "A steady rhythm. The repository is maintaining a healthy pace.")
        self.assertEqual(vital_signs.get_heartbeat_diagnosis(5.5), "The code is buzzing with activity! Keep up the good work, little bots!")
        self.assertEqual(vital_signs.get_heartbeat_diagnosis(8.0), "A frantic pace! The repository is on fire! (In a good way, hopefully!)")

    @patch('vital_signs.get_commit_count', return_value=14)
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_success(self, mock_exit, mock_stdout, mock_get_commit_count):
        vital_signs.main()
        mock_get_commit_count.assert_called_once_with(7)
        expected_output_part = "Commit Heartbeat: 2.0 commits/day\nDiagnosis: A steady rhythm. The repository is maintaining a healthy pace.\n"
        self.assertIn(expected_output_part, mock_stdout.getvalue())
        mock_exit.assert_called_once_with(0)

    @patch('vital_signs.get_commit_count', return_value=-1)
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_error_path(self, mock_exit, mock_stdout, mock_get_commit_count):
        vital_signs.main()
        mock_get_commit_count.assert_called_once_with(7)
        expected_output_part = "Diagnosis: Failed to retrieve commit data. Please check logs for errors.\n"
        self.assertIn(expected_output_part, mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
