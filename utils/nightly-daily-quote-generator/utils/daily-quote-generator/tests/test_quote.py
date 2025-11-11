import importlib.util
import pathlib
from unittest import mock


def _load_quote_module():
    """Dynamically load the `quote.py` module without requiring it to be a package."""
    file_path = pathlib.Path(__file__).resolve().parents[1] / "src" / "quote.py"
    spec = importlib.util.spec_from_file_location("quote", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    return module


def test_get_random_quote_deterministic():
    # Mock rationale: patch `random.choice` to always return the first element, making the test deterministic.
    with mock.patch("random.choice", lambda seq: seq[0]):
        quote_mod = _load_quote_module()
        result = quote_mod.get_random_quote()
        assert result == (
            "The only limit to our realization of tomorrow is our doubts of today.",
            "Franklin D. Roosevelt",
        )


def test_format_quote():
    quote_mod = _load_quote_module()
    formatted = quote_mod.format_quote("Test quote", "Author")
    expected = '"Test quote"\n    — Author'
    assert formatted == expected
