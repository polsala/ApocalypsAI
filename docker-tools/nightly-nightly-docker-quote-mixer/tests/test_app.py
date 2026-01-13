import json
import builtins
from unittest import mock

# Mock rationale: we replace random.choice to return predictable values so the test is deterministic and offline.

def test_mix_quote_deterministic():
    import src.app as app_module
    with mock.patch('random.choice') as mock_choice:
        # First call returns inspirational, second call returns apocalyptic
        mock_choice.side_effect = ["Believe in the impossible", "Mutant crows watch over you"]
        result = app_module.mix_quote()
        assert result == "Believe in the impossible – Mutant crows watch over you"

def test_get_quote_endpoint():
    from src import app
    client = app.app.test_client()
    # Mock random.choice to control output
    with mock.patch('random.choice') as mock_choice:
        mock_choice.side_effect = ["Hope is the strongest weapon", "The last bunker is opening"]
        response = client.get('/quote')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["quote"] == "Hope is the strongest weapon – The last bunker is opening"

