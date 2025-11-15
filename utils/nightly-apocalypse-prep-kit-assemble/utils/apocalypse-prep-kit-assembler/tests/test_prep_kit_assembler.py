import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import tempfile
import shutil
import subprocess

# Add the src directory to the path to allow importing the utility
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from prep_kit_assembler import assemble_prep_kit

class TestPrepKitAssembler(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.requirements_file = os.path.join(self.test_dir, 'requirements.txt')
        self.output_dir = os.path.join(self.test_dir, 'offline_packages')

        # Create a dummy requirements file
        with open(self.requirements_file, 'w') as f:
            f.write('requests==2.28.1\n')
            f.write('pyyaml==6.0\n')

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    @patch('subprocess.run')
    @patch('os.makedirs')
    @patch('builtins.print')
    def test_assemble_prep_kit_success(self, mock_print, mock_makedirs, mock_subprocess_run):
        # Mock rationale: subprocess.run is an external process call (pip download).
        # We want to test the Python logic around it, not actually download packages.
        # Mocking it allows deterministic, fast, and offline testing.
        mock_subprocess_run.return_value = MagicMock(
            returncode=0,
            stdout="Successfully downloaded packages.",
            stderr=""
        )

        assemble_prep_kit(self.requirements_file, self.output_dir)

        mock_makedirs.assert_called_once_with(self.output_dir, exist_ok=True)
        mock_subprocess_run.assert_called_once_with(
            [sys.executable, '-m', 'pip', 'download', '-r', self.requirements_file, '-d', self.output_dir],
            check=True,
            capture_output=True,
            text=True
        )
        mock_print.assert_any_call(f"Successfully assembled prep kit in '{self.output_dir}'.")

    @patch('subprocess.run')
    @patch('os.makedirs')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_assemble_prep_kit_requirements_file_not_found(self, mock_sys_exit, mock_print, mock_makedirs, mock_subprocess_run):
        # Mock rationale: sys.exit is called to terminate the script on error.
        # Mocking it prevents actual script termination during testing.
        # We test that it would have been called with the correct error code.
        non_existent_file = os.path.join(self.test_dir, 'non_existent.txt')

        assemble_prep_kit(non_existent_file, self.output_dir)

        mock_print.assert_any_call(f"Error: Requirements file not found at '{non_existent_file}'", file=sys.stderr)
        mock_sys_exit.assert_called_once_with(1)
        mock_makedirs.assert_not_called()
        mock_subprocess_run.assert_not_called()

    @patch('subprocess.run')
    @patch('os.makedirs')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_assemble_prep_kit_pip_failure(self, mock_sys_exit, mock_print, mock_makedirs, mock_subprocess_run):
        # Mock rationale: Simulates a non-zero exit code from pip, indicating a failure.
        # This tests the error handling path for subprocess.CalledProcessError.
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd=[sys.executable, '-m', 'pip', 'download', '-r', self.requirements_file, '-d', self.output_dir],
            stdout="",
            stderr="ERROR: Could not find a version that satisfies the requirement non_existent_package"
        )

        assemble_prep_kit(self.requirements_file, self.output_dir)

        mock_makedirs.assert_called_once_with(self.output_dir, exist_ok=True)
        mock_subprocess_run.assert_called_once()
        mock_print.assert_any_call(unittest.mock.ANY, file=sys.stderr) # Check for error print
        mock_sys_exit.assert_called_once_with(1)

    @patch('subprocess.run')
    @patch('os.makedirs')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_assemble_prep_kit_pip_command_not_found(self, mock_sys_exit, mock_print, mock_makedirs, mock_subprocess_run):
        # Mock rationale: Simulates the 'pip' command not being found, e.g., if Python/pip is not in PATH.
        # This tests the FileNotFoundError handling path.
        mock_subprocess_run.side_effect = FileNotFoundError("No such file or directory: 'pip'")

        assemble_prep_kit(self.requirements_file, self.output_dir)

        mock_makedirs.assert_called_once_with(self.output_dir, exist_ok=True)
        mock_subprocess_run.assert_called_once()
        mock_print.assert_any_call("Error: 'pip' command not found. Ensure Python and pip are installed and in your PATH.", file=sys.stderr)
        mock_sys_exit.assert_called_once_with(1)

    @patch('subprocess.run')
    @patch('os.makedirs')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_assemble_prep_kit_unexpected_error(self, mock_sys_exit, mock_print, mock_makedirs, mock_subprocess_run):
        # Mock rationale: Simulates any other unexpected exception during the process.
        # This tests the general Exception handling path.
        mock_subprocess_run.side_effect = ValueError("Something unexpected happened")

        assemble_prep_kit(self.requirements_file, self.output_dir)

        mock_makedirs.assert_called_once_with(self.output_dir, exist_ok=True)
        mock_subprocess_run.assert_called_once()
        mock_print.assert_any_call("An unexpected error occurred: Something unexpected happened", file=sys.stderr)
        mock_sys_exit.assert_called_once_with(1)
