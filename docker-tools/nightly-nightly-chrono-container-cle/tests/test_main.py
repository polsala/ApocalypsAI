import pytest
import os
import sys
import datetime
from unittest.mock import patch, mock_open, MagicMock
from io import StringIO

# Add the src directory to the path for importing main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import main

# --- Mock Rationale ---
# We need to mock file system operations (os.walk, open) to simulate project structures
# and file contents without actually creating files.
# We need to mock external network requests (requests.get) to avoid actual API calls
# and ensure deterministic, offline tests.
# We need to mock Docker SDK calls (docker.from_env().images.get) to simulate local
# Docker daemon responses without requiring a running Docker daemon.
# We also mock sys.stdout to capture printed output for assertions.

# Mock data for Docker Hub API responses
MOCK_DOCKER_HUB_RESPONSE_FRESH = {
    "last_updated": (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)).isoformat()
}
MOCK_DOCKER_HUB_RESPONSE_DUSTY = {
    "last_updated": (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=400)).isoformat()
}
MOCK_DOCKER_HUB_RESPONSE_NOT_FOUND = {
    "detail": "Not found"
}

# Mock data for local Docker inspect responses
MOCK_LOCAL_IMAGE_FRESH = {
    'Created': (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=60)).timestamp()
}
MOCK_LOCAL_IMAGE_DUSTY = {
    'Created': (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=500)).timestamp()
}

@pytest.fixture
def mock_filesystem():
    """Mocks os.walk and open for file system operations."""
    mock_walk_data = [
        ('/project', ['subdir1', 'subdir2'], ['Dockerfile', 'docker-compose.yml']),
        ('/project/subdir1', [], ['Dockerfile']),
        ('/project/subdir2', [], ['another.txt']),
    ]
    with patch('os.walk', return_value=mock_walk_data), \
         patch('builtins.open', new_callable=mock_open) as mock_file:
        yield mock_file

@pytest.fixture
def mock_docker_client():
    """Mocks the docker client and its image methods."""
    with patch('main.docker.from_env') as mock_from_env:
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_client.images.get.side_effect = main.docker.errors.ImageNotFound("No such image") # Default to not found locally
        yield mock_client

@pytest.fixture
def mock_requests_get():
    """Mocks requests.get for Docker Hub API calls."""
    with patch('main.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None # No HTTP errors by default
        mock_response.json.return_value = MOCK_DOCKER_HUB_RESPONSE_FRESH # Default to fresh
        mock_get.return_value = mock_response
        yield mock_get

@pytest.fixture
def capsys_stdout(capsys):
    """Fixture to capture stdout."""
    yield capsys

def test_find_docker_files(mock_filesystem):
    docker_files, docker_compose_files = main.find_docker_files('/project')
    assert sorted(docker_files) == sorted(['/project/Dockerfile', '/project/subdir1/Dockerfile'])
    assert sorted(docker_compose_files) == sorted(['/project/docker-compose.yml'])

def test_extract_images_from_dockerfile(mock_filesystem):
    mock_filesystem.side_effect = [
        mock_open(read_data="FROM python:3.9-slim\nRUN apt-get update\nFROM alpine:3.14 AS builder").return_value
    ]
    images = main.extract_images_from_dockerfile('/project/Dockerfile')
    assert sorted(images) == sorted(['python:3.9-slim', 'alpine:3.14'])

def test_extract_images_from_docker_compose(mock_filesystem):
    mock_filesystem.side_effect = [
        mock_open(read_data="""
version: '3.8'
services:
  web:
    image: nginx:1.21
    ports:
      - "80:80"
  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: app_db
""").return_value
    ]
    images = main.extract_images_from_docker_compose('/project/docker-compose.yml')
    assert sorted(images) == sorted(['nginx:1.21', 'postgres:13-alpine'])

def test_get_image_age_local_fresh(mock_docker_client):
    mock_image = MagicMock()
    mock_image.attrs = MOCK_LOCAL_IMAGE_FRESH
    mock_docker_client.images.get.return_value = mock_image

    age = main.get_image_age("my-local-image:latest")
    assert age is not None
    assert age.tzinfo is not None # Ensure timezone-aware datetime

def test_get_image_age_local_dusty(mock_docker_client):
    mock_image = MagicMock()
    mock_image.attrs = MOCK_LOCAL_IMAGE_DUSTY
    mock_docker_client.images.get.return_value = mock_image

    age = main.get_image_age("my-local-image:old")
    assert age is not None
    assert age.tzinfo is not None

def test_get_image_age_docker_hub_fresh(mock_docker_client, mock_requests_get):
    # Local not found, fall back to Docker Hub
    mock_docker_client.images.get.side_effect = main.docker.errors.ImageNotFound("No such image")
    mock_requests_get.return_value.json.return_value = MOCK_DOCKER_HUB_RESPONSE_FRESH

    age = main.get_image_age("nginx:latest")
    assert age is not None
    assert age.tzinfo is not None
    mock_requests_get.assert_called_once() # Ensure Docker Hub was called

def test_get_image_age_docker_hub_dusty(mock_docker_client, mock_requests_get):
    # Local not found, fall back to Docker Hub
    mock_docker_client.images.get.side_effect = main.docker.errors.ImageNotFound("No such image")
    mock_requests_get.return_value.json.return_value = MOCK_DOCKER_HUB_RESPONSE_DUSTY

    age = main.get_image_age("ubuntu:18.04")
    assert age is not None
    assert age.tzinfo is not None
    mock_requests_get.assert_called_once()

def test_get_image_age_not_found(mock_docker_client, mock_requests_get):
    # Local not found, Docker Hub also not found
    mock_docker_client.images.get.side_effect = main.docker.errors.ImageNotFound("No such image")
    mock_requests_get.return_value.json.return_value = MOCK_DOCKER_HUB_RESPONSE_NOT_FOUND
    mock_requests_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

    age = main.get_image_age("nonexistent-image:latest")
    assert age is None
    mock_requests_get.assert_called_once()

@patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/project', threshold_days=365))
def test_main_no_images_found(mock_args, mock_filesystem, capsys_stdout):
    # Configure mock_filesystem to return no Dockerfiles or docker-compose files
    mock_filesystem.return_value = mock_open(read_data="").return_value # Ensure open doesn't fail
    with patch('os.walk', return_value=[]): # No files found
        main.main()
        captured = capsys_stdout.readouterr()
        assert "No Docker images found" in captured.out

@patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/project', threshold_days=180))
def test_main_with_dusty_and_fresh_images(mock_args, mock_filesystem, mock_docker_client, mock_requests_get, capsys_stdout):
    # Simulate a project with Dockerfiles and docker-compose
    mock_walk_data = [
        ('/project', [], ['Dockerfile', 'docker-compose.yml']),
    ]
    with patch('os.walk', return_value=mock_walk_data):
        # Mock file contents
        mock_filesystem.side_effect = [
            # Dockerfile content
            mock_open(read_data="FROM dusty_image:1.0\nFROM fresh_image:latest").return_value,
            # docker-compose.yml content
            mock_open(read_data="""
version: '3.8'
services:
  app:
    image: another_dusty_image:2.0
  worker:
    image: another_fresh_image:dev
""").return_value
        ]

        # Mock get_image_age for specific images
        def mock_get_image_age_side_effect(image_name):
            if "dusty_image" in image_name:
                return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=400)
            elif "fresh_image" in image_name:
                return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)
            elif "another_dusty_image" in image_name:
                return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=200)
            elif "another_fresh_image" in image_name:
                return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=10)
            return None

        with patch('main.get_image_age', side_effect=mock_get_image_age_side_effect):
            main.main()
            captured = capsys_stdout.readouterr()

            assert "DUSTY IMAGES DETECTED" in captured.out
            assert "dusty_image:1.0" in captured.out
            assert "another_dusty_image:2.0" in captured.out
            assert "Fresh as a daisy! Last updated" in captured.out
            assert "fresh_image:latest" in captured.out
            assert "another_fresh_image:dev" in captured.out
            assert "Suggestions for a 'freshening' ritual" in captured.out
            assert "2 DUSTY IMAGES DETECTED" in captured.out # Check count

@patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/project', threshold_days=180))
def test_main_all_fresh_images(mock_args, mock_filesystem, mock_docker_client, mock_requests_get, capsys_stdout):
    mock_walk_data = [
        ('/project', [], ['Dockerfile']),
    ]
    with patch('os.walk', return_value=mock_walk_data):
        mock_filesystem.side_effect = [
            mock_open(read_data="FROM fresh_image_a:latest\nFROM fresh_image_b:1.0").return_value,
        ]

        def mock_get_image_age_side_effect(image_name):
            return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=90) # All fresh

        with patch('main.get_image_age', side_effect=mock_get_image_age_side_effect):
            main.main()
            captured = capsys_stdout.readouterr()

            assert "All detected container images are sparkling fresh!" in captured.out
            assert "DUSTY IMAGES DETECTED" not in captured.out
            assert "fresh_image_a:latest" in captured.out
            assert "fresh_image_b:1.0" in captured.out

@patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='/project', threshold_days=180))
def test_main_with_unknown_age_images(mock_args, mock_filesystem, capsys_stdout):
    mock_walk_data = [
        ('/project', [], ['Dockerfile']),
    ]
    with patch('os.walk', return_value=mock_walk_data):
        mock_filesystem.side_effect = [
            mock_open(read_data="FROM unknown_image:latest").return_value,
        ]

        with patch('main.get_image_age', return_value=None): # Simulate unknown age
            main.main()
            captured = capsys_stdout.readouterr()

            assert "Age unknown. Perhaps a relic from a forgotten era?" in captured.out
            assert "unknown_image:latest" in captured.out
            assert "DUSTY IMAGES DETECTED" not in captured.out # Unknown age is not "dusty"
