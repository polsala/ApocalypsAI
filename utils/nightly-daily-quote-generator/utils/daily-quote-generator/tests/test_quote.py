import datetime
import hashlib
import importlib.util
import pathlib

# Mock rationale: we replace the file‑system loader with a deterministic in‑memory list of quotes.
MOCK_QUOTES = [
    {"quote": "Test quote A", "author": "Author A"},
    {"quote": "Test quote B", "author": "Author B"},
    {"quote": "Test quote C", "author": "Author C"},
]


def _load_module():
    """Dynamically load the ``quote.py`` module from the sibling ``src`` directory."""
    src_path = pathlib.Path(__file__).resolve().parents[1] / "src" / "quote.py"
    spec = importlib.util.spec_from_file_location("quote", src_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_get_quote_fixed_date(monkeypatch):
    # Mock rationale: force a known date and inject the mock quote list.
    fixed_date = datetime.date(2023, 1, 1)
    mod = _load_module()
    monkeypatch.setattr(mod, "load_quotes", lambda: MOCK_QUOTES)
    result = mod.get_quote(fixed_date)
    expected_idx = int(
        hashlib.sha256(fixed_date.isoformat().encode()).hexdigest(), 16
    ) % len(MOCK_QUOTES)
    expected = f"{MOCK_QUOTES[expected_idx]['quote']} — {MOCK_QUOTES[expected_idx]['author']}"
    assert result == expected


def test_main_prints_quote(monkeypatch, capsys):
    # Mock rationale: capture stdout of the CLI entry point while controlling date and data.
    fake_today = datetime.date(2022, 12, 31)
    mod = _load_module()
    monkeypatch.setattr(mod, "load_quotes", lambda: MOCK_QUOTES)
    monkeypatch.setattr(datetime.date, "today", lambda: fake_today)
    mod.main()
    captured = capsys.readouterr()
    expected_idx = int(
        hashlib.sha256(fake_today.isoformat().encode()).hexdigest(), 16
    ) % len(MOCK_QUOTES)
    expected = f"{MOCK_QUOTES[expected_idx]['quote']} — {MOCK_QUOTES[expected_idx]['author']}\n"
    assert captured.out == expected
