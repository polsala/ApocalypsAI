from unittest import mock

# Mock rationale: Verify that the core function returns an element from the list
# and that the list contains the expected number of compliments.

def test_get_random_compliment_returns_valid_item(monkeypatch):
    import random_compliment.core as core
    # Force deterministic choice
    with mock.patch('random.choice', lambda seq: seq[-1]):
        result = core.get_random_compliment()
        assert result == core._COMPLIMENTS[-1]
    # Ensure the list length is as defined
    assert len(core._COMPLIMENTS) == 5
