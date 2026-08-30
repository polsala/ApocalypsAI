import pytest
import json
import datetime
from unittest.mock import patch

# Import the Flask app from the source directory
import sys
sys.path.append('src')
import app as flask_app

@pytest.fixture
def client():
    flask_app.app.config['TESTING'] = True
    with flask_app.app.test_client() as client:
        # Clear messages before each test to ensure isolation
        with flask_app.message_lock:
            flask_app.messages.clear()
        yield client

# Mock rationale: We need to control the current time to test message expiration
# without actually waiting for real time to pass. This ensures deterministic tests.
@patch('datetime.datetime')
def test_send_message_success(mock_datetime, client):
    mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0)
    mock_datetime.timedelta = datetime.timedelta # Mock rationale: timedelta is a class, not a method, so we pass it through

    response = client.post('/send', json={
        'sender': 'Alice',
        'recipient': 'Bob',
        'message': 'Hello Bob!',
        'ttl_seconds': 60
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'Message sent' in data['status']
    assert 'message_id' in data

    with flask_app.message_lock:
        assert 'Bob' in flask_app.messages
        assert len(flask_app.messages['Bob']) == 1
        assert flask_app.messages['Bob'][0]['sender'] == 'Alice'
        assert flask_app.messages['Bob'][0]['message'] == 'Hello Bob!'
        assert flask_app.messages['Bob'][0]['expires_at'] == datetime.datetime(2023, 1, 1, 10, 1, 0)

@patch('datetime.datetime')
def test_send_message_missing_fields(mock_datetime, client):
    mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0) # Mock rationale: Consistent time for all tests
    mock_datetime.timedelta = datetime.timedelta

    response = client.post('/send', json={
        'sender': 'Alice',
        'recipient': 'Bob',
        'ttl_seconds': 60
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Missing required fields' in data['error']

@patch('datetime.datetime')
def test_send_message_invalid_ttl(mock_datetime, client):
    mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0) # Mock rationale: Consistent time for all tests
    mock_datetime.timedelta = datetime.timedelta

    response = client.post('/send', json={
        'sender': 'Alice',
        'recipient': 'Bob',
        'message': 'Hello Bob!',
        'ttl_seconds': 'not_an_int'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'ttl_seconds must be an integer' in data['error']

    response = client.post('/send', json={
        'sender': 'Alice',
        'recipient': 'Bob',
        'message': 'Hello Bob!',
        'ttl_seconds': 0
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'ttl_seconds must be a positive integer' in data['error']

@patch('datetime.datetime')
def test_receive_messages_no_messages(mock_datetime, client):
    mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0) # Mock rationale: Consistent time for all tests
    mock_datetime.timedelta = datetime.timedelta

    response = client.get('/receive/Charlie')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == []

@patch('datetime.datetime')
def test_receive_messages_success_and_deletion(mock_datetime, client):
    mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0) # Mock rationale: Set initial time
    mock_datetime.timedelta = datetime.timedelta

    # Send a message
    client.post('/send', json={
        'sender': 'Alice',
        'recipient': 'Bob',
        'message': 'First message',
        'ttl_seconds': 60
    })
    client.post('/send', json={
        'sender': 'Charlie',
        'recipient': 'Bob',
        'message': 'Second message',
        'ttl_seconds': 120
    })

    # Advance time slightly for received_at timestamp to be different
    mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 5)

    # Receive messages for Bob
    response = client.get('/receive/Bob')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['message'] == 'First message'
    assert data[1]['message'] == 'Second message'
    assert data[0]['received_at'] == '2023-01-01T10:00:05'

    # Verify messages are deleted after retrieval
    with flask_app.message_lock:
        assert 'Bob' not in flask_app.messages

    # Try to receive again, should be empty
    response = client.get('/receive/Bob')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == []

@patch('datetime.datetime')
def test_message_expiration(mock_datetime, client):
    mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0) # Mock rationale: Set initial time
    mock_datetime.timedelta = datetime.timedelta

    # Send a message with a short TTL
    client.post('/send', json={
        'sender': 'Alice',
        'recipient': 'Bob',
        'message': 'Ephemeral message',
        'ttl_seconds': 5
    })

    # Advance time past the TTL
    mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 10) # Mock rationale: Simulate time passing

    # Try to receive the message, should be empty
    response = client.get('/receive/Bob')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == []

    # Verify message is gone from store
    with flask_app.message_lock:
        assert 'Bob' not in flask_app.messages

@patch('datetime.datetime')
def test_multiple_recipients(mock_datetime, client):
    mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0) # Mock rationale: Consistent time for all tests
    mock_datetime.timedelta = datetime.timedelta

    client.post('/send', json={'sender': 'Alice', 'recipient': 'Bob', 'message': 'To Bob', 'ttl_seconds': 60})
    client.post('/send', json={'sender': 'Alice', 'recipient': 'Charlie', 'message': 'To Charlie', 'ttl_seconds': 60})

    response_bob = client.get('/receive/Bob')
    assert response_bob.status_code == 200
    data_bob = json.loads(response_bob.data)
    assert len(data_bob) == 1
    assert data_bob[0]['message'] == 'To Bob'

    response_charlie = client.get('/receive/Charlie')
    assert response_charlie.status_code == 200
    data_charlie = json.loads(response_charlie.data)
    assert len(data_charlie) == 1
    assert data_charlie[0]['message'] == 'To Charlie'

    with flask_app.message_lock:
        assert 'Bob' not in flask_app.messages
        assert 'Charlie' not in flask_app.messages

@patch('datetime.datetime')
def test_cleanup_on_send(mock_datetime, client):
    mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0) # Mock rationale: Set initial time
    mock_datetime.timedelta = datetime.timedelta

    # Send an expired message
    client.post('/send', json={
        'sender': 'OldBot',
        'recipient': 'ExpiredUser',
        'message': 'This should expire',
        'ttl_seconds': 1
    })

    # Advance time past its TTL
    mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 5) # Mock rationale: Simulate time passing

    # Send a new message to trigger cleanup
    client.post('/send', json={
        'sender': 'NewBot',
        'recipient': 'ActiveUser',
        'message': 'New message',
        'ttl_seconds': 60
    })

    # Verify the expired message's recipient is not in messages anymore
    with flask_app.message_lock:
        assert 'ExpiredUser' not in flask_app.messages
        assert 'ActiveUser' in flask_app.messages
        assert len(flask_app.messages['ActiveUser']) == 1
