import datetime
import sys
import pathlib

# Ensure the src directory is on the import path
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from quote import get_quote, _QUOTES

def test_get_quote_fixed_date():
    """# Mock rationale: use a fixed date to guarantee deterministic output"""
    fixed_date = datetime.date(2023, 1, 1)
    assert get_quote(date=fixed_date) == "When the mind is still, the universe surrenders."

def test_get_quote_with_theme():
    """# Mock rationale: theme "silence" matches a single quote, ensuring filtering works"""
    fixed_date = datetime.date(2023, 1, 2)
    assert get_quote(date=fixed_date, theme="silence") == "Silence is a source of great strength."

def test_get_quote_theme_no_match_fallback():
    """# Mock rationale: nonexistent theme forces fallback to full list"""
    fixed_date = datetime.date(2023, 1, 3)
    quote = get_quote(date=fixed_date, theme="nonexistent")
    seed = fixed_date.toordinal() + hash("nonexistent")
    expected = _QUOTES[seed % len(_QUOTES)]
    assert quote == expected
