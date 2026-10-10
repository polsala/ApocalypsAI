import pytest
from src.app import app, readings

@pytest.fixture(autouse=True)
def clear_readings():
    # Ensure a clean state before each test
    readings.clear()
    yield
    readings.clear()

def test_add_reading_success():
    client = app.test_client()
    response = client.post("/reading", json={"value": 4.2})
    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "ok"
    assert readings == [4.2]

def test_add_reading_missing_value():
    client = app.test_client()
    response = client.post("/reading", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_average_calculation():
    client = app.test_client()
    client.post("/reading", json={"value": 2.0})
    client.post("/reading", json={"value": 4.0})
    resp = client.get("/average")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["average"] == 3.0
    assert data["count"] == 2

def test_average_no_readings():
    client = app.test_client()
    resp = client.get("/average")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["average"] is None
    assert data["count"] == 0
