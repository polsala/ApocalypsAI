import json
from src import app as flask_app

def test_quote_endpoint(monkeypatch):
    # Mock random.choice to return a deterministic quote
    def mock_choice(_):
        return "Test quote for unit testing."
    monkeypatch.setattr("random.choice", mock_choice)

    client = flask_app.app.test_client()
    response = client.get("/quote")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["quote"] == "Test quote for unit testing."
