import pytest
import json
from unittest.mock import patch
from src.app import app, COMFORT_IMAGES, SOOTHING_QUOTES

@pytest.fixture
def client():
    """Configures the Flask app for testing."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """
    Test the /health endpoint returns a 200 OK and expected status.
    """
    response = client.get('/health')
    assert response.status_code == 200
    assert json.loads(response.data) == {"status": "Critter is purring!"}

@patch('random.choice')
def test_get_comfort_endpoint(mock_random_choice, client):
    """
    Test the /comfort endpoint returns expected data with mocked random choices.
    # Mock rationale: Ensures deterministic test results by controlling random selections.
    """
    # Configure mock_random_choice to return specific items in order
    mock_random_choice.side_effect = [
        COMFORT_IMAGES[0],  # First call for image_url
        SOOTHING_QUOTES[0]  # Second call for quote
    ]

    response = client.get('/comfort')
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "image_url" in data
    assert "quote" in data
    assert "message" in data
    assert data["image_url"] == COMFORT_IMAGES[0]
    assert data["quote"] == SOOTHING_QUOTES[0]
    assert data["message"] == "May this bring a moment of peace to your apocalyptic day!"

    # Ensure random.choice was called twice
    assert mock_random_choice.call_count == 2

@patch('random.choice')
def test_get_comfort_endpoint_different_choices(mock_random_choice, client):
    """
    Test the /comfort endpoint with different mocked random choices.
    # Mock rationale: Ensures deterministic test results by controlling random selections.
    """
    mock_random_choice.side_effect = [
        COMFORT_IMAGES[1],  # First call for image_url
        SOOTHING_QUOTES[1]  # Second call for quote
    ]

    response = client.get('/comfort')
    assert response.status_code == 200
    data = json.loads(response.data)

    assert data["image_url"] == COMFORT_IMAGES[1]
    assert data["quote"] == SOOTHING_QUOTES[1]
    assert data["message"] == "May this bring a moment of peace to your apocalyptic day!"

    assert mock_random_choice.call_count == 2
