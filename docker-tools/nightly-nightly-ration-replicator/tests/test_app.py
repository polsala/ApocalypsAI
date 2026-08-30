import pytest
from src.app import app, rations, whimsical_facts
from datetime import datetime, timedelta
import json

# Mock rationale: The Flask test client allows simulating HTTP requests
# without running a live server, making tests deterministic and offline.
# We also clear the in-memory 'rations' list before each test to ensure
# test isolation and determinism.
# For date-based checks, we use a fixed 'today' for comparison to avoid
# non-deterministic results based on the actual current date. pytest.MonkeyPatch
# is used to temporarily override datetime.now() for these specific tests.

@pytest.fixture
def client():
    """Configures the Flask app for testing."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Clear rations before each test to ensure a clean state
        rations.clear()
        yield client

def test_home_page(client):
    """Test the home page returns a welcome message."""
    response = client.get('/')
    assert response.status_code == 200
    assert "Welcome to the Nightly Ration Replicator!" in response.data.decode()

def test_add_ration_success(client):
    """Test adding a ration successfully."""
    ration_data = {
        "name": "Canned Tuna",
        "quantity": 3,
        "expiry": "2025-10-20",
        "calories_per_unit": 150
    }
    response = client.post('/rations', json=ration_data)
    assert response.status_code == 201
    assert "Ration added successfully" in response.json['message']
    assert len(rations) == 1
    assert rations[0]['name'] == "Canned Tuna"

def test_add_ration_missing_field(client):
    """Test adding a ration with a missing field."""
    ration_data = {
        "name": "Canned Tuna",
        "quantity": 3,
        "expiry": "2025-10-20"
        # Missing calories_per_unit
    }
    response = client.post('/rations', json=ration_data)
    assert response.status_code == 400
    assert "Missing data" in response.json['error']
    assert len(rations) == 0

def test_add_ration_invalid_expiry_format(client):
    """Test adding a ration with an invalid expiry date format."""
    ration_data = {
        "name": "Canned Tuna",
        "quantity": 3,
        "expiry": "2025/10/20", # Invalid format
        "calories_per_unit": 150
    }
    response = client.post('/rations', json=ration_data)
    assert response.status_code == 400
    assert "Invalid data format or value" in response.json['error']
    assert len(rations) == 0

def test_add_ration_invalid_quantity(client):
    """Test adding a ration with an invalid quantity."""
    ration_data = {
        "name": "Canned Tuna",
        "quantity": -1, # Invalid quantity
        "expiry": "2025-10-20",
        "calories_per_unit": 150
    }
    response = client.post('/rations', json=ration_data)
    assert response.status_code == 400
    assert "Invalid data format or value" in response.json['error']
    assert len(rations) == 0

def test_list_rations_empty(client):
    """Test listing rations when none are added."""
    response = client.get('/rations')
    assert response.status_code == 200
    assert response.json == []

def test_list_rations_with_items(client):
    """Test listing rations with existing items."""
    rations.append({"name": "MRE", "quantity": 1, "expiry": "2026-01-01", "calories_per_unit": 1200})
    rations.append({"name": "Water Tabs", "quantity": 10, "expiry": "2024-12-31", "calories_per_unit": 0})
    
    response = client.get('/rations')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['name'] == "MRE"
    assert response.json[1]['name'] == "Water Tabs"

def test_get_whimsical_fact(client):
    """Test getting a whimsical fact."""
    response = client.get('/fact')
    assert response.status_code == 200
    assert "fact" in response.json
    assert response.json['fact'] in whimsical_facts

def test_check_expiry_no_param(client):
    """Test expiry check without 'days' parameter."""
    response = client.get('/expiry')
    assert response.status_code == 400
    assert "Please provide a positive 'days' parameter" in response.json['error']

def test_check_expiry_invalid_param(client):
    """Test expiry check with invalid 'days' parameter."""
    response = client.get('/expiry?days=0')
    assert response.status_code == 400
    assert "Please provide a positive 'days' parameter" in response.json['error']
    
    response = client.get('/expiry?days=abc') # Flask's type converter handles this
    assert response.status_code == 400
    assert "Please provide a positive 'days' parameter" in response.json['error']

@pytest.fixture
def client_with_fixed_rations(client):
    """Configures the Flask app for testing with pre-populated rations and a fixed 'today'."""
    # Add items relative to a fixed 'today' for deterministic testing
    fixed_today = datetime(2024, 6, 15).date()
    rations.extend([
        {"name": "Expired Item", "quantity": 1, "expiry": "2024-06-10", "calories_per_unit": 100}, # Expired
        {"name": "Expiring Soon", "quantity": 2, "expiry": "2024-07-10", "calories_per_unit": 200}, # Expires in < 30 days
        {"name": "Expiring Later", "quantity": 3, "expiry": "2024-09-15", "calories_per_unit": 300}, # Expires in exactly 90 days
        {"name": "Long Shelf Life", "quantity": 4, "expiry": "2025-06-15", "calories_per_unit": 400}, # Expires in 1 year
        {"name": "Expires Today", "quantity": 1, "expiry": "2024-06-15", "calories_per_unit": 50} # Expires today
    ])
    yield client

def test_check_expiry_scenarios(client_with_fixed_rations):
    """Test expiry check with various scenarios using a fixed date."""
    fixed_today = datetime(2024, 6, 15).date() 

    with pytest.MonkeyPatch().context() as mp:
        mp.setattr(datetime, 'now', lambda: datetime(fixed_today.year, fixed_today.month, fixed_today.day))

        # Test for items expiring within 30 days
        response = client_with_fixed_rations.get('/expiry?days=30')
        assert response.status_code == 200
        expiring_items = response.json
        assert len(expiring_items) == 2 # Expiring Soon, Expires Today
        assert any(item['name'] == "Expiring Soon" for item in expiring_items)
        assert any(item['name'] == "Expires Today" for item in expiring_items)

        # Test for items expiring within 90 days
        response = client_with_fixed_rations.get('/expiry?days=90')
        assert response.status_code == 200
        expiring_items = response.json
        assert len(expiring_items) == 3 # Expiring Soon, Expiring Later, Expires Today
        assert any(item['name'] == "Expiring Soon" for item in expiring_items)
        assert any(item['name'] == "Expiring Later" for item in expiring_items)
        assert any(item['name'] == "Expires Today" for item in expiring_items)

        # Test for items expiring within 1 day (includes today and tomorrow)
        response = client_with_fixed_rations.get('/expiry?days=1')
        assert response.status_code == 200
        expiring_items = response.json
        assert len(expiring_items) == 1 # Only "Expires Today"
        assert expiring_items[0]['name'] == "Expires Today"
