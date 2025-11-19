import builtins
import types
import pytest

# Import the module under test
from utils.nightly_quote_of_the_day.src.quote_of_the_day import get_random_quote


class MockRandom:
    """A minimal mock of ``random.Random`` exposing only ``choice``.

    # Mock rationale: deterministic selection of the first element ensures
    # the test does not depend on actual randomness and runs offline.
    """

    def __init__(self, sequence):
        self._seq = sequence

    def choice(self, _):
        # Always return the first element of the original quote list.
        return self._seq[0]


def test_get_random_quote_deterministic(monkeypatch):
    # Import the internal quote list via a private attribute.
    import importlib
    mod = importlib.import_module(
        "utils.nightly_quote_of_the_day.src.quote_of_the_day"
    )
    quotes = mod._QUOTES

    mock_rng = MockRandom(quotes)
    result = get_random_quote(rng=mock_rng)
    assert result == quotes[0]


def test_cli_output(capsys, monkeypatch):
    # Run the module as a script with a fixed seed to get reproducible output.
    import importlib
    mod = importlib.import_module(
        "utils.nightly_quote_of_the_day.src.quote_of_the_day"
    )
    monkeypatch.setattr(
        mod, "__name__", "__main__"
    )
    # Simulate command‑line arguments
    monkeypatch.setattr(
        builtins, "__argv__", ["quote_of_the_day.py", "--seed", "42"]
    )
    # Execute main()
    mod.main()
    captured = capsys.readouterr()
    # With seed 42, the random choice is deterministic; we just ensure output is a string.
    assert isinstance(captured.out.strip(), str)
    assert captured.out.strip() != ""
