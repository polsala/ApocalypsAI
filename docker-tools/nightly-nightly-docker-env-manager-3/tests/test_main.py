import pytest
import subprocess
from unittest.mock import patch, MagicMock
import os

# Mock the main script to avoid actual Docker operations during tests
# We'll mock subprocess.run to control its behavior

# Mock rationale: These tests are designed to be deterministic and offline.
# They mock the subprocess.run function to simulate Docker commands without
# actually interacting with the Docker daemon. This ensures tests run quickly,
# reliably, and without external dependencies.

@patch('subprocess.run')
def test_run_command_success(mock_subprocess_run):
    """Tests successful execution of a command."""
    mock_result = MagicMock()
    mock_result.stdout = "Success output\n"
    mock_result.stderr = ""
    mock_result.returncode = 0
    mock_subprocess_run.return_value = mock_result

    from src.main import run_command
    output = run_command("echo 'Hello'")
    assert output == "Success output\n"
    mock_subprocess_run.assert_called_once_with(
        ['echo', "'Hello'"], shell=True, check=True, capture_output=True, text=True
    )

@patch('subprocess.run')
def test_run_command_failure(mock_subprocess_run):
    """Tests failed execution of a command."""
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd="ls non_existent_dir", output="", stderr="ls: cannot access 'non_existent_dir': No such file or directory"
    )

    from src.main import run_command
    with pytest.raises(SystemExit):
        run_command("ls non_existent_dir")

@patch('src.main.run_command')
def test_build_docker_image_success(mock_run_command):
    """Tests successful Docker image build."""
    # Mock os.path.isdir and os.path.exists to simulate a valid environment
    with patch('os.path.isdir', return_value=True),
         patch('os.path.exists', return_value=True),
         patch('os.path.join', return_value='/fake/path/Dockerfile'):
        from src.main import build_docker_image
        build_docker_image("my-test-env")
        mock_run_command.assert_called_once_with("docker build -t apoc-my-test-env-env /fake/path")

@patch('src.main.run_command')
def test_build_docker_image_env_not_found(mock_run_command):
    """Tests building Docker image when environment directory is not found."""
    with patch('os.path.isdir', return_value=False):
        from src.main import build_docker_image
        with pytest.raises(SystemExit):
            build_docker_image("non-existent-env")
        mock_run_command.assert_not_called()

@patch('src.main.run_command')
def test_build_docker_image_dockerfile_not_found(mock_run_command):
    """Tests building Docker image when Dockerfile is not found."""
    with patch('os.path.isdir', return_value=True),
         patch('os.path.exists', return_value=False),
         patch('os.path.join', return_value='/fake/path/Dockerfile'):
        from src.main import build_docker_image
        with pytest.raises(SystemExit):
            build_docker_image("my-test-env")
        mock_run_command.assert_not_called()

@patch('src.main.run_command')
def test_start_environment_with_compose(mock_run_command):
    """Tests starting an environment using docker-compose."""
    # Mock os.path.exists for docker-compose.yml and os.chdir
    with patch('os.path.exists', side_effect=lambda p: p.endswith('docker-compose.yml')),
         patch('os.path.abspath', return_value='/fake/env/dir'),
         patch('os.getcwd', return_value='/current/dir'),
         patch('os.chdir') as mock_chdir:
        from src.main import start_environment
        start_environment("my-compose-env")
        mock_chdir.assert_any_call('/fake/env/dir')
        mock_chdir.assert_any_call('/current/dir')
        mock_run_command.assert_called_once_with("docker-compose up -d")

@patch('src.main.run_command')
def test_start_environment_without_compose(mock_run_command):
    """Tests starting an environment without docker-compose."""
    # Mock os.path.exists for docker-compose.yml to return False
    with patch('os.path.exists', return_value=False),
         patch('os.path.abspath', return_value='/fake/env/dir'):
        from src.main import start_environment
        start_environment("my-direct-env")
        mock_run_command.assert_called_once_with("docker run --rm -it -v $(pwd):/app apoc-my-direct-env-env")

@patch('src.main.run_command')
def test_stop_environment_with_compose(mock_run_command):
    """Tests stopping an environment using docker-compose."""
    with patch('os.path.exists', side_effect=lambda p: p.endswith('docker-compose.yml')),
         patch('os.path.abspath', return_value='/fake/env/dir'),
         patch('os.getcwd', return_value='/current/dir'),
         patch('os.chdir') as mock_chdir:
        from src.main import stop_environment
        stop_environment("my-compose-env")
        mock_chdir.assert_any_call('/fake/env/dir')
        mock_chdir.assert_any_call('/current/dir')
        mock_run_command.assert_called_once_with("docker-compose down")

@patch('src.main.run_command')
def test_stop_environment_without_compose(mock_run_command):
    """Tests stopping an environment without docker-compose."""
    with patch('os.path.exists', return_value=False),
         patch('os.path.abspath', return_value='/fake/env/dir'):
        from src.main import stop_environment
        stop_environment("my-direct-env")
        mock_run_command.assert_not_called()

@patch('src.main.start_environment')
@patch('src.main.stop_environment')
@patch('src.main.build_docker_image')
def test_main_start_command(mock_build, mock_stop, mock_start):
    """Tests the main function with the 'start' command."""
    with patch('sys.argv', ['src/main.py', 'start', 'my-env']):
        from src.main import main
        main()
        mock_start.assert_called_once_with('my-env')
        mock_build.assert_not_called()
        mock_stop.assert_not_called()

@patch('src.main.start_environment')
@patch('src.main.stop_environment')
@patch('src.main.build_docker_image')
def test_main_stop_command(mock_build, mock_stop, mock_start):
    """Tests the main function with the 'stop' command."""
    with patch('sys.argv', ['src/main.py', 'stop', 'my-env']):
        from src.main import main
        main()
        mock_stop.assert_called_once_with('my-env')
        mock_build.assert_not_called()
        mock_start.assert_not_called()

@patch('src.main.start_environment')
@patch('src.main.stop_environment')
@patch('src.main.build_docker_image')
def test_main_build_command(mock_build, mock_stop, mock_start):
    """Tests the main function with the 'build' command."""
    with patch('sys.argv', ['src/main.py', 'build', 'my-env']):
        from src.main import main
        main()
        mock_build.assert_called_once_with('my-env')
        mock_stop.assert_not_called()
        mock_start.assert_not_called()

@patch('src.main.start_environment')
@patch('src.main.stop_environment')
@patch('src.main.build_docker_image')
def test_main_invalid_command(mock_build, mock_stop, mock_start):
    """Tests the main function with an invalid command."""
    with patch('sys.argv', ['src/main.py', 'run', 'my-env']),
         pytest.raises(SystemExit):
        from src.main import main
        main()
        mock_build.assert_not_called()
        mock_stop.assert_not_called()
        mock_start.assert_not_called()

@patch('src.main.start_environment')
@patch('src.main.stop_environment')
@patch('src.main.build_docker_image')
def test_main_insufficient_args(mock_build, mock_stop, mock_start):
    """Tests the main function with insufficient arguments."""
    with patch('sys.argv', ['src/main.py', 'start']),
         pytest.raises(SystemExit):
        from src.main import main
        main()
        mock_build.assert_not_called()
        mock_stop.assert_not_called()
        mock_start.assert_not_called()
