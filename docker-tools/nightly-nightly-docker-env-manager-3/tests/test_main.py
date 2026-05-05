import pytest
import docker
from unittest.mock import patch, MagicMock
import os

# Mock the docker client and its methods
@pytest.fixture
def mock_docker_client():
    with patch('docker.from_env') as mock_client_factory:
        mock_client = MagicMock()
        mock_client_factory.return_value = mock_client
        yield mock_client

# Mock the os module for file existence checks
@pytest.fixture
def mock_os_path():
    with patch('os.path.exists') as mock_exists:
        yield mock_exists

# Mock the yaml module for loading config
@pytest.fixture
def mock_yaml_load():
    with patch('yaml.safe_load') as mock_load:
        yield mock_load

# Mock subprocess for potential external calls (though not directly used in current main.py)
@pytest.fixture
def mock_subprocess():
    with patch('subprocess.run') as mock_run:
        yield mock_run

# Helper to create a mock container object
def create_mock_container(container_id='mock_container_id', name='mock_env', status='running'):
    mock_container = MagicMock()
    mock_container.id = container_id
    mock_container.name = name
    mock_container.status = status
    mock_container.logs.return_value = b"Mock log output\n"
    mock_container.exec_run.return_value.exit_code = 0
    mock_container.exec_run.return_value.output = b""
    return mock_container

def test_load_config_success(mock_yaml_load, mock_os_path):
    from src.main import DockerEnvManager
    mock_os_path.return_value = True
    mock_config_data = {
        'name': 'test-env',
        'image': 'test-image:latest',
        'ports': ['8080:80'],
        'volumes': ['/host/path:/container/path']
    }
    mock_yaml_load.return_value = mock_config_data

    manager = DockerEnvManager(env_config_path='test_env.yaml')
    assert manager.config == mock_config_data

def test_load_config_not_found(mock_os_path):
    from src.main import DockerEnvManager
    mock_os_path.return_value = False
    with pytest.raises(SystemExit) as excinfo:
        DockerEnvManager(env_config_path='non_existent.yaml')
    assert excinfo.value.code == 1

def test_up_container_already_running(mock_docker_client, mock_yaml_load, mock_os_path):
    from src.main import DockerEnvManager
    mock_os_path.return_value = True
    mock_yaml_load.return_value = {'name': 'existing-env', 'image': 'test-image'}
    mock_container = create_mock_container(name='apoc-existing-env')
    mock_docker_client.containers.get.return_value = mock_container

    manager = DockerEnvManager()
    manager.up()

    mock_docker_client.containers.run.assert_not_called() # Should not try to run if already exists

def test_up_new_container(mock_docker_client, mock_yaml_load, mock_os_path):
    from src.main import DockerEnvManager
    mock_os_path.return_value = True
    mock_config = {
        'name': 'new-dev',
        'image': 'python:3.11-slim',
        'ports': ['8000:8000'],
        'volumes': ['.:/app'],
        'commands': ['echo "hello"']
    }
    mock_yaml_load.return_value = mock_config
    mock_container = create_mock_container(name='apoc-new-dev', status='created')
    mock_docker_client.containers.get.side_effect = docker.errors.NotFound(404, 'Not Found')
    mock_docker_client.containers.run.return_value = mock_container

    manager = DockerEnvManager()
    manager.up()

    mock_docker_client.containers.run.assert_called_once_with(
        'python:3.11-slim',
        detach=True,
        name='apoc-new-dev',
        ports={'8000': '8000'},
        volumes={'/app': {'bind': '/app', 'mode': 'rw'}},
        tty=True,
        stdin_open=True
    )
    mock_container.exec_run.assert_called_once_with('echo "hello"')

def test_up_image_not_found(mock_docker_client, mock_yaml_load, mock_os_path):
    from src.main import DockerEnvManager
    mock_os_path.return_value = True
    mock_config = {'name': 'bad-image-env', 'image': 'non-existent-image'}
    mock_yaml_load.return_value = mock_config
    mock_docker_client.containers.get.side_effect = docker.errors.NotFound(404, 'Not Found')
    mock_docker_client.containers.run.side_effect = docker.errors.ImageNotFound('Image not found')

    manager = DockerEnvManager()
    with pytest.raises(SystemExit) as excinfo:
        manager.up()
    assert excinfo.value.code == 1

def test_down_container_running(mock_docker_client, mock_yaml_load, mock_os_path):
    from src.main import DockerEnvManager
    mock_os_path.return_value = True
    mock_yaml_load.return_value = {'name': 'to-be-stopped'}
    mock_container = create_mock_container(name='apoc-to-be-stopped')
    mock_docker_client.containers.get.return_value = mock_container

    manager = DockerEnvManager()
    manager.down()

    mock_container.stop.assert_called_once()
    mock_container.remove.assert_called_once()

def test_down_container_not_running(mock_docker_client, mock_yaml_load, mock_os_path):
    from src.main import DockerEnvManager
    mock_os_path.return_value = True
    mock_yaml_load.return_value = {'name': 'not-running'}
    mock_docker_client.containers.get.side_effect = docker.errors.NotFound(404, 'Not Found')

    manager = DockerEnvManager()
    manager.down()

    # No calls to stop or remove should happen
    mock_docker_client.containers.get.assert_called_once()

def test_logs_container_running(mock_docker_client, mock_yaml_load, mock_os_path):
    from src.main import DockerEnvManager
    mock_os_path.return_value = True
    mock_yaml_load.return_value = {'name': 'log-env'}
    mock_container = create_mock_container(name='apoc-log-env')
    mock_docker_client.containers.get.return_value = mock_container

    manager = DockerEnvManager()
    manager.logs()

    mock_container.logs.assert_called_once()

def test_logs_container_not_running(mock_docker_client, mock_yaml_load, mock_os_path):
    from src.main import DockerEnvManager
    mock_os_path.return_value = True
    mock_yaml_load.return_value = {'name': 'log-not-running'}
    mock_docker_client.containers.get.side_effect = docker.errors.NotFound(404, 'Not Found')

    manager = DockerEnvManager()
    manager.logs()

    mock_docker_client.containers.get.assert_called_once()

# Mock rationale: These tests simulate the behavior of the docker-py library and the os/yaml modules
# without requiring actual Docker daemon interaction or file system access. This ensures deterministic,
# offline testing of the DockerEnvManager logic.
