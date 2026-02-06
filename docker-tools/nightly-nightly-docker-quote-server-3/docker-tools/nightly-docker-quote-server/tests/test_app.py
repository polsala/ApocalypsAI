import json
from unittest import mock
from src.app import app, QUOTES

def test_quote_endpoint():
    with mock.patch('random.choice', return_value=QUOTES[0]):
        client = app.test_client()
        response = client.get("/quote")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {"quote": QUOTES[0]}
