import pytest
from unittest import mock
from src import app as app_module

@pytest.fixture
def client():
    app_module.app.testing = True
    with app_module.app.test_client() as client:
        yield client

def test_mood_morning(client):
    with mock.patch.object(app_module, "get_hour", return_value=8):
        resp = client.get("/mood")
        assert resp.status_code == 200
        assert resp.get_json() == {"emoji": "🌞"}

def test_mood_afternoon(client):
    with mock.patch.object(app_module, "get_hour", return_value=14):
        resp = client.get("/mood")
        assert resp.status_code == 200
        assert resp.get_json() == {"emoji": "☕"}

def test_mood_evening(client):
    with mock.patch.object(app_module, "get_hour", return_value=19):
        resp = client.get("/mood")
        assert resp.status_code == 200
        assert resp.get_json() == {"emoji": "🌙"}

def test_mood_night(client):
    with mock.patch.object(app_module, "get_hour", return_value=23):
        resp = client.get("/mood")
        assert resp.status_code == 200
        assert resp.get_json() == {"emoji": "⭐"}
