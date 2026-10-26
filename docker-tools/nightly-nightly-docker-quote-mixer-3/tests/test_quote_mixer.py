import json
from unittest import mock

from src.quote_mixer import get_mixed_quote

def test_get_mixed_quote_deterministic():
    # Mock random.choice to always return the first element of each list
    with mock.patch('src.quote_mixer.random.choice', side_effect=lambda seq: seq[0]):
        quote = get_mixed_quote()
        assert quote == "The ash whispers your name. Believe in yourself."

def test_flask_endpoint():
    from src.app import app
    client = app.test_client()
    # Mock get_mixed_quote to return a known string
    with mock.patch('src.app.get_mixed_quote', return_value="Mocked quote"):
        response = client.get("/quote")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["quote"] == "Mocked quote"
