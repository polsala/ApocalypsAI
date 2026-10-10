import json
from src.app import app, QUOTES

def test_quote_endpoint():
    client = app.test_client()
    response = client.get("/quote")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "quote" in data
    # Mock rationale: ensure returned quote is from predefined list
    assert data["quote"] in QUOTES
