import pytest
import os
from unittest.mock import patch, mock_open
from src.app import app, STATIC_DIR_PATH # Import the new STATIC_DIR_PATH

@pytest.fixture
def client():
    """Configures the Flask app for testing."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_no_files(client):
    """
    Test the index page when no static files are present.
    # Mock rationale: os.listdir is mocked to simulate an empty static directory
    # without needing to create/delete actual files, ensuring deterministic tests.
    # os.path.isfile is mocked to ensure no files are considered.
    """
    with patch('os.listdir', return_value=[]), \
         patch('os.path.isfile', return_value=False):
        response = client.get('/')
        assert response.status_code == 200
        assert b"No broadcasts found. The airwaves are silent..." in response.data
        assert b"Nightly Broadcast Beacon" in response.data

def test_index_with_files(client):
    """
    Test the index page when static files are present.
    # Mock rationale: os.listdir is mocked to simulate specific files in the static directory
    # without needing to create actual files, ensuring deterministic tests.
    # os.path.isfile is mocked to confirm these mocked files are treated as regular files.
    """
    mock_files = ['message_01.txt', 'ambient_winds.txt']
    # When os.path.isfile is called, it will be with the full path, e.g., /app/src/static/message_01.txt
    # So the side_effect needs to reflect that.
    mock_full_paths = [os.path.join(STATIC_DIR_PATH, f) for f in mock_files]
    with patch('os.listdir', return_value=mock_files), \
         patch('os.path.isfile', side_effect=lambda x: x in mock_full_paths):
        response = client.get('/')
        assert response.status_code == 200
        assert b"message_01.txt" in response.data
        assert b"ambient_winds.txt" in response.data
        assert b"No broadcasts found" not in response.data

def test_broadcast_file_exists(client):
    """
    Test serving an existing broadcast file.
    # Mock rationale: send_from_directory is mocked to prevent actual file system access
    # and simulate a successful file serving, ensuring deterministic tests.
    """
    with patch('src.app.send_from_directory', return_value="File content simulated") as mock_send:
        response = client.get('/broadcast/test_message.txt')
        assert response.status_code == 200
        assert response.data == b"File content simulated"
        # send_from_directory is called with app.static_folder, which is STATIC_DIR_PATH
        mock_send.assert_called_with(STATIC_DIR_PATH, 'test_message.txt')

def test_broadcast_file_not_found(client):
    """
    Test serving a non-existent broadcast file (Flask's send_from_directory handles 404).
    # Mock rationale: send_from_directory is mocked to raise a NotFound exception,
    # simulating a file not being found by the underlying Flask mechanism.
    """
    from werkzeug.exceptions import NotFound
    with patch('src.app.send_from_directory', side_effect=NotFound) as mock_send:
        response = client.get('/broadcast/non_existent.txt')
        assert response.status_code == 404
        mock_send.assert_called_with(STATIC_DIR_PATH, 'non_existent.txt')

def test_static_dir_creation_on_main_run():
    """
    Test that the static directory is created when app.py is run directly.
    # Mock rationale: os.path.exists and os.makedirs are mocked to prevent actual file system
    # modifications during the test, ensuring a clean and deterministic test environment.
    # open is mocked to prevent actual file creation.
    """
    with patch('os.path.exists', return_value=False) as mock_exists, \
         patch('os.makedirs') as mock_makedirs, \
         patch('builtins.open', mock_open()) as mock_file_open:
        # We need to ensure app.run() is not called, as it blocks.
        with patch('src.app.app.run'):
            # Reload the module to trigger the __name__ == '__main__' block
            # This is a common pattern for testing main blocks.
            import importlib
            import src.app as app_module
            importlib.reload(app_module) # Reload to re-execute the main block

        mock_exists.assert_called_with(STATIC_DIR_PATH)
        mock_makedirs.assert_called_with(STATIC_DIR_PATH)
        mock_file_open.assert_any_call(os.path.join(STATIC_DIR_PATH, 'message_01.txt'), 'w')
        mock_file_open.assert_any_call(os.path.join(STATIC_DIR_PATH, 'ambient_winds.txt'), 'w')
