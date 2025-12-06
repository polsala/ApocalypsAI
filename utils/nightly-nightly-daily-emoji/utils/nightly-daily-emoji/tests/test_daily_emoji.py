import hashlib
import pytest
from daily_emoji import get_daily_emoji

def test_consistency():
    """Same input yields same output."""
    date = "2023-07-15"
    first = get_daily_emoji(date)
    second = get_daily_emoji(date)
    assert first == second

def test_different_dates():
    """Different dates most likely produce different emojis (non‑collision)."""
    emoji1 = get_daily_emoji("2023-07-15")
    emoji2 = get_daily_emoji("2023-07-16")
    assert emoji1 != emoji2

def test_mocked_hash(monkeypatch):
    """# Mock rationale: force a known hash to verify index calculation."""
    class DummyHash:
        def hexdigest(self):
            # First 8 hex chars are all zeros -> index 0
            return "00000000deadbeefcafebabe1234567890abcdef1234567890abcdef12345678"
    def dummy_sha256(_):
        return DummyHash()
    monkeypatch.setattr(hashlib, "sha256", dummy_sha256)
    assert get_daily_emoji("any-date") == "😀"
