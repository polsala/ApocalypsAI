import pytest
from src.app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_quote_endpoint(client):
    response = client.get("/quote")
    assert response.status_code == 200
    data = response.get_json()
    expected = "The only limit to our realization of tomorrow is our doubts of today. The sky is falling, but the coffee is still hot."
    assert data["quote"] == expected
