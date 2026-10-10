import datetime
import pytest
from src import app as flask_app

@pytest.fixture
def client():
    flask_app.app.testing = True
    with flask_app.app.test_client() as client:
        yield client

def test_mood_morning(monkeypatch, client):
    class FixedDatetime(datetime.datetime):
        @classmethod
        def utcnow(cls):
            return cls(2023, 1, 1, 9, 0, 0)  # 9 AM UTC
    monkeypatch.setattr(datetime, "datetime", FixedDatetime)
    resp = client.get("/mood")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["hour"] == 9
    assert data["emoji"] == ["☕", "🌅", "😊"]

def test_mood_evening(monkeypatch, client):
    class FixedDatetime(datetime.datetime):
        @classmethod
        def utcnow(cls):
            return cls(2023, 1, 1, 20, 0, 0)  # 8 PM UTC
    monkeypatch.setattr(datetime, "datetime", FixedDatetime)
    resp = client.get("/mood")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["hour"] == 20
    assert data["emoji"] == ["🌆", "🌙", "🍷"]
