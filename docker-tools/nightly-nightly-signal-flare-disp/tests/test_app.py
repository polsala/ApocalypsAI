import json
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

# Import the Flask app from the src directory
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app import app, SIGNAL_STRENGTHS, ATMOSPHERIC_CONDITIONS, FLARE_COLORS, FLARE_TRAJECTORIES, RESPONSE_TIMES

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.uuid.uuid4')
@patch('app.datetime')
@patch('app.random.choice')
@patch('app.random.randint')
def test_dispatch_flare_success(mock_randint, mock_choice, mock_datetime, mock_uuid4, client):
    # Mock rationale: Ensure deterministic output for random choices and UUID/datetime.
    # This allows tests to predict the exact response content.

    # Mock datetime for predictable transmission_id
    mock_datetime.now.return_value = datetime(2024, 7, 29, 10, 30, 0)
    mock_datetime.now.strftime.return_value = '20240729'

    # Mock uuid for predictable transmission_id
    mock_uuid_obj = MagicMock()
    mock_uuid_obj.hex = 'abcdef1234567890'
    mock_uuid4.return_value = mock_uuid_obj

    # Mock random choices for predictable report generation
    mock_choice.side_effect = [
        SIGNAL_STRENGTHS[0],      # signal_strength
        FLARE_COLORS[0],          # flare_color
        FLARE_TRAJECTORIES[0],    # flare_trajectory
        ATMOSPHERIC_CONDITIONS[0], # atmospheric_condition
        RESPONSE_TIMES[0]         # response_time
    ]

    # Mock random randint for predictable estimated_arrival_time_s
    mock_randint.return_value = 120

    response = client.post(
        '/dispatch_flare',
        data=json.dumps({"message": "Test message", "sector": "Test Sector"}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)

    expected_report = (
        f"A shimmering {FLARE_COLORS[0]} flare {FLARE_TRAJECTORIES[0]}, carrying your plea. "
        f"Atmospheric interference was caused by {ATMOSPHERIC_CONDITIONS[0]}, "
        f"but the message appears to have reached the general vicinity of Test Sector. "
        f"{RESPONSE_TIMES[0]}"
    )

    assert data == {
        "status": "Flare Dispatched",
        "transmission_id": "FLARE-20240729-ABCDEF12",
        "target_sector": "Test Sector",
        "message_sent": "Test message",
        "report": expected_report,
        "signal_strength": SIGNAL_STRENGTHS[0],
        "estimated_arrival_time_s": 120
    }

def test_dispatch_flare_missing_message(client):
    response = client.post(
        '/dispatch_flare',
        data=json.dumps({"sector": "Test Sector"}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data == {"error": "Missing 'message' or 'sector' in request body."}

def test_dispatch_flare_missing_sector(client):
    response = client.post(
        '/dispatch_flare',
        data=json.dumps({"message": "Test message"}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data == {"error": "Missing 'message' or 'sector' in request body."}

def test_dispatch_flare_empty_body(client):
    response = client.post(
        '/dispatch_flare',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data == {"error": "Missing 'message' or 'sector' in request body."}

def test_dispatch_flare_no_json_body(client):
    response = client.post(
        '/dispatch_flare',
        data="not json",
        content_type='text/plain'
    )
    # Flask's request.get_json() returns None if content-type is not application/json
    # or if the JSON is invalid. This should trigger the missing data check.
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data == {"error": "Missing 'message' or 'sector' in request body."}
