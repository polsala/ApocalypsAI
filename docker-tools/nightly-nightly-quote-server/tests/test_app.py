import json
from src.app import app, QUOTES

def test_root_returns_quote():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "quote" in data
    assert data["quote"] in QUOTES
