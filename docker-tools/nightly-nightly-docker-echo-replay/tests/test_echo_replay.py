import pytest
import json
import subprocess
import os
import sys
from unittest.mock import patch, mock_open
from io import StringIO

# Import the functions to be tested
from echo_replay import record_command_output, replay_command_output

# Mock rationale: We need to test the logic of record_command_output and replay_command_output
# without actually interacting with the Docker daemon or writing/reading real files.
# subprocess.run is mocked to simulate Docker command execution.
# open is mocked to simulate file system interactions.
# sys.stdout and sys.stderr are mocked to capture printed output.

@pytest.fixture
def mock_subprocess_run():
    """Fixture to mock subprocess.run for Docker commands."""
    with patch('subprocess.run') as mock_run:
        yield mock_run

@pytest.fixture
def mock_open_file():
    """Fixture to mock open() for file operations."""
    with patch('builtins.open', mock_open()) as mock_file:
        yield mock_file

@pytest.fixture
def mock_stdout_stderr():
    """Fixture to capture stdout and stderr."""
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
         patch('sys.stderr', new_callable=StringIO) as mock_stderr:
        yield mock_stdout, mock_stderr

def test_record_command_output_success(mock_subprocess_run, mock_open_file, mock_stdout_stderr):
    """Test successful recording of command output."""
    # Mock rationale: Simulate a successful Docker command execution.
    mock_subprocess_run.return_value = subprocess.CompletedProcess(
        args=["docker", "run", "--rm", "test_image", "bash", "-c", "echo hello"],
        returncode=0,
        stdout="Hello from container\n",
        stderr="Warning: something happened\n"
    )

    image = "test_image"
    command = "echo hello"
    output_file = "test_output.json"

    record_command_output(image, command, output_file)

    # Verify subprocess.run was called correctly
    mock_subprocess_run.assert_called_once_with(
        ["docker", "run", "--rm", image, "bash", "-c", command],
        capture_output=True,
        text=True,
        check=False
    )

    # Verify file was opened for writing
    mock_open_file.assert_called_once_with(output_file, 'w')

    # Verify content written to file
    written_content = json.loads(mock_open_file().write.call_args[0][0])
    assert written_content["stdout"] == "Hello from container\n"
    assert written_content["stderr"] == "Warning: something happened\n"
    assert written_content["exit_code"] == 0
    assert written_content["image"] == image
    assert written_content["command"] == command
    assert "timestamp" in written_content

    # Verify console output
    stdout, stderr = mock_stdout_stderr
    assert "Recording command" in stdout.getvalue()
    assert "Successfully recorded output" in stdout.getvalue()
    assert "Exit Code: 0" in stdout.getvalue()
    assert not stderr.getvalue()

def test_record_command_output_non_zero_exit(mock_subprocess_run, mock_open_file, mock_stdout_stderr):
    """Test recording of command output with a non-zero exit code."""
    # Mock rationale: Simulate a Docker command failing with a non-zero exit code.
    mock_subprocess_run.return_value = subprocess.CompletedProcess(
        args=["docker", "run", "--rm", "test_image", "bash", "-c", "exit 1"],
        returncode=1,
        stdout="",
        stderr="Error: command failed\n"
    )

    image = "test_image"
    command = "exit 1"
    output_file = "test_error_output.json"

    record_command_output(image, command, output_file)

    # Verify subprocess.run was called correctly
    mock_subprocess_run.assert_called_once()

    # Verify file was opened for writing
    mock_open_file.assert_called_once_with(output_file, 'w')

    # Verify content written to file
    written_content = json.loads(mock_open_file().write.call_args[0][0])
    assert written_content["stdout"] == ""
    assert written_content["stderr"] == "Error: command failed\n"
    assert written_content["exit_code"] == 1

    # Verify console output
    stdout, stderr = mock_stdout_stderr
    assert "Recording command" in stdout.getvalue()
    assert "Successfully recorded output" in stdout.getvalue()
    assert "Exit Code: 1" in stdout.getvalue()
    assert not stderr.getvalue()

def test_record_command_output_docker_not_found(mock_subprocess_run, mock_stdout_stderr):
    """Test case where 'docker' command is not found."""
    # Mock rationale: Simulate FileNotFoundError if 'docker' command is not in PATH.
    mock_subprocess_run.side_effect = FileNotFoundError

    image = "test_image"
    command = "echo hello"
    output_file = "test_output.json"

    with pytest.raises(SystemExit) as excinfo:
        record_command_output(image, command, output_file)
    assert excinfo.value.code == 1

    stdout, stderr = mock_stdout_stderr
    assert "Error: 'docker' command not found" in stderr.getvalue()

def test_replay_command_output_success(mock_open_file, mock_stdout_stderr):
    """Test successful replaying of recorded output."""
    recorded_data = {
        "stdout": "Line 1\nLine 2\n",
        "stderr": "Error line 1\n",
        "exit_code": 0,
        "image": "ubuntu:latest",
        "command": "ls -l",
        "timestamp": 1678886400.0
    }
    # Mock rationale: Simulate reading a valid JSON file.
    mock_open_file.return_value.__enter__.return_value.read.return_value = json.dumps(recorded_data)

    input_file = "test_input.json"
    replay_command_output(input_file, delay=0) # Set delay to 0 for faster testing

    # Verify file was opened for reading
    mock_open_file.assert_called_once_with(input_file, 'r')

    # Verify console output
    stdout, stderr = mock_stdout_stderr
    expected_stdout = (
        "Replaying output from test_input.json...\n"
        "\n--- Replay of 'ls -l' from 'ubuntu:latest' ---\n"
        "\n--- STDOUT ---\n"
        "Line 1\n"
        "Line 2\n\n"
        "\n--- STDERR ---\n"
        "Error line 1\n\n"
        "--- Replay Finished (Simulated Exit Code: 0) ---\n\n"
    )
    # The actual output might have slight variations due to print statements and newlines.
    # Let's check for key phrases and order.
    assert "Replaying output from test_input.json..." in stdout.getvalue()
    assert "--- Replay of 'ls -l' from 'ubuntu:latest' ---" in stdout.getvalue()
    assert "--- STDOUT ---" in stdout.getvalue()
    assert "Line 1\nLine 2\n" in stdout.getvalue()
    assert "--- STDERR ---" in stdout.getvalue()
    assert "Error line 1\n" in stderr.getvalue() # stderr should go to sys.stderr
    assert "--- Replay Finished (Simulated Exit Code: 0) ---" in stdout.getvalue()

def test_replay_command_output_no_stderr(mock_open_file, mock_stdout_stderr):
    """Test replaying output when no stderr was recorded."""
    recorded_data = {
        "stdout": "Only stdout here\n",
        "stderr": "",
        "exit_code": 0,
        "image": "alpine",
        "command": "cat /etc/os-release",
        "timestamp": 1678886400.0
    }
    # Mock rationale: Simulate reading a valid JSON file with no stderr.
    mock_open_file.return_value.__enter__.return_value.read.return_value = json.dumps(recorded_data)

    input_file = "test_input_no_stderr.json"
    replay_command_output(input_file, delay=0)

    stdout, stderr = mock_stdout_stderr
    assert "Only stdout here\n" in stdout.getvalue()
    assert "--- STDERR ---" not in stdout.getvalue() # Should not print stderr section
    assert not stderr.getvalue() # No stderr should be printed

def test_replay_command_output_file_not_found(mock_open_file, mock_stdout_stderr):
    """Test replaying when the input file does not exist."""
    # Mock rationale: Simulate FileNotFoundError when opening the input file.
    mock_open_file.side_effect = FileNotFoundError

    input_file = "non_existent.json"
    with pytest.raises(SystemExit) as excinfo:
        replay_command_output(input_file)
    assert excinfo.value.code == 1

    stdout, stderr = mock_stdout_stderr
    assert f"Error: Input file '{input_file}' not found." in stderr.getvalue()

def test_replay_command_output_invalid_json(mock_open_file, mock_stdout_stderr):
    """Test replaying when the input file contains invalid JSON."""
    # Mock rationale: Simulate a JSONDecodeError when loading the input file.
    mock_open_file.return_value.__enter__.return_value.read.return_value = "this is not json"

    input_file = "invalid.json"
    with pytest.raises(SystemExit) as excinfo:
        replay_command_output(input_file)
    assert excinfo.value.code == 1

    stdout, stderr = mock_stdout_stderr
    assert f"Error: Could not decode JSON from '{input_file}'." in stderr.getvalue()
