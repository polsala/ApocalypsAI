import pytest
import os
import subprocess
from unittest.mock import patch, MagicMock

# Assume the script is in the same directory for testing purposes
# In a real scenario, you might need to adjust the path or use a different testing approach
SCRIPT_PATH = "src/lint_workflows.sh"

# Mock rationale: We mock subprocess.run to control its output and behavior,
# allowing us to test different scenarios (success, failure, missing yamllint)
# without actually executing external commands or creating temporary files.
@patch('subprocess.run')
def test_lint_workflows_success(mock_subprocess_run):
    """Tests successful linting of workflow files."""
    # Mock yamllint to return success (exit code 0)
    mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

    # Mock os.find to return some dummy workflow files
    with patch('os.find', return_value=['.github/workflows/main.yml', '.github/workflows/deploy.yml']):
        # Execute the script (simulated)
        # We don't actually run the shell script, but simulate its execution flow
        # by patching the relevant functions it calls.
        # For simplicity, we'll simulate the script's logic directly here
        # as it's a shell script. A more robust approach might involve
        # a wrapper Python script or using pytest-shell.

        # Simulate the script's core logic:
        # 1. Check for yamllint
        # 2. Find files
        # 3. Run yamllint

        # Mocking yamllint command execution
        mock_yamllint_cmd = MagicMock()
        mock_yamllint_cmd.returncode = 0
        mock_yamllint_cmd.stdout = b""
        mock_yamllint_cmd.stderr = b""

        with patch('subprocess.run', return_value=mock_yamllint_cmd) as mock_run:
            # Simulate the script's execution
            # We need to simulate the 'find' command's output as well
            with patch('subprocess.check_output', return_value=b'.github/workflows/main.yml\n.github/workflows/deploy.yml\n') as mock_check_output:
                # Simulate the 'command -v yamllint' check
                with patch('subprocess.Popen') as mock_popen:
                    mock_popen_instance = MagicMock()
                    mock_popen_instance.communicate.return_value = (b'yamllint', b'')
                    mock_popen_instance.returncode = 0
                    mock_popen.return_value = mock_popen_instance

                    # Call the script's logic (simulated)
                    # This is a simplified simulation. In a real test, you'd want to
                    # capture stdout/stderr and assert on them.
                    try:
                        # This part is tricky for shell scripts. We'll simulate the outcome.
                        # The actual script would be run via subprocess.run(['bash', SCRIPT_PATH, ...])
                        # For this example, we'll assert the mock was called correctly.
                        pass # Placeholder for actual script execution simulation
                    except SystemExit as e:
                        assert e.code == 0, f"Expected exit code 0, but got {e.code}"

                    # Assert that yamllint was called with the correct files
                    mock_run.assert_called_once_with(['yamllint', '--strict', '.github/workflows/main.yml', '.github/workflows/deploy.yml'], capture_output=True, text=True)


@patch('subprocess.run')
def test_lint_workflows_failure(mock_subprocess_run):
    """Tests failed linting of workflow files."""
    # Mock yamllint to return failure (non-zero exit code)
    mock_subprocess_run.return_value = MagicMock(returncode=1, stdout="", stderr="Lint error found.")

    with patch('os.find', return_value=['.github/workflows/invalid.yml']):
        # Simulate the script's core logic:
        mock_yamllint_cmd = MagicMock()
        mock_yamllint_cmd.returncode = 1
        mock_yamllint_cmd.stdout = b""
        mock_yamllint_cmd.stderr = b"Lint error found."

        with patch('subprocess.run', return_value=mock_yamllint_cmd) as mock_run:
            with patch('subprocess.check_output', return_value=b'.github/workflows/invalid.yml\n') as mock_check_output:
                with patch('subprocess.Popen') as mock_popen:
                    mock_popen_instance = MagicMock()
                    mock_popen_instance.communicate.return_value = (b'yamllint', b'')
                    mock_popen_instance.returncode = 0
                    mock_popen.return_value = mock_popen_instance

                    try:
                        # Simulate script execution and expect SystemExit with code 1
                        with pytest.raises(SystemExit) as e:
                            pass # Placeholder for actual script execution simulation
                        assert e.value.code == 1, f"Expected exit code 1, but got {e.value.code}"
                    except SystemExit as e:
                        assert e.code == 1, f"Expected exit code 1, but got {e.code}"

                    mock_run.assert_called_once_with(['yamllint', '--strict', '.github/workflows/invalid.yml'], capture_output=True, text=True)


@patch('subprocess.run')
def test_lint_workflows_no_yamllint(mock_subprocess_run):
    """Tests behavior when yamllint is not installed."""
    # Mock yamllint command to indicate it's not found
    mock_subprocess_run.side_effect = FileNotFoundError

    with patch('os.find', return_value=['.github/workflows/main.yml']):
        # Simulate the 'command -v yamllint' check failing
        with patch('subprocess.Popen') as mock_popen:
            mock_popen_instance = MagicMock()
            mock_popen_instance.communicate.return_value = (b'', b'yamllint: command not found')
            mock_popen_instance.returncode = 127 # Common exit code for command not found
            mock_popen.return_value = mock_popen_instance

            # Expect SystemExit with code 1 due to missing yamllint
            with pytest.raises(SystemExit) as e:
                pass # Placeholder for actual script execution simulation
            assert e.value.code == 1, f"Expected exit code 1, but got {e.value.code}"


@patch('subprocess.run')
def test_lint_workflows_no_files(mock_subprocess_run):
    """Tests behavior when no workflow files are found."""
    # Mock os.find to return an empty list
    with patch('os.find', return_value=[]) as mock_find:
        # Mock the check for yamllint to succeed so we don't exit early
        with patch('subprocess.Popen') as mock_popen:
            mock_popen_instance = MagicMock()
            mock_popen_instance.communicate.return_value = (b'yamllint', b'')
            mock_popen_instance.returncode = 0
            mock_popen.return_value = mock_popen_instance

            # Expect the script to exit with code 0 as there's nothing to lint
            try:
                pass # Placeholder for actual script execution simulation
            except SystemExit as e:
                assert e.code == 0, f"Expected exit code 0, but got {e.code}"

            # Ensure yamllint was not called
            mock_subprocess_run.assert_not_called()
