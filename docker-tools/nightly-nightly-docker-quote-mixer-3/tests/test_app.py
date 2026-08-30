import json
import random
from src.app import app as flask_app

def test_quote_endpoint():
    random.seed(0)
    client = flask_app.test_client()
    response = client.get("/quote")
    assert response.status_code == 200
    data = json.loads(response.data)
    expected = "The sun rises, but the shadows linger."
    assert data["quote"] == expected
