import datetime
import builtins
from types import SimpleNamespace

# Mock rationale: we replace datetime.datetime.now with a deterministic value
# so the test does not depend on the actual current time or the system clock.

# Import the module under test
from src.clock import render_time, main


def _mock_datetime(target: datetime.datetime):
    """Return a SimpleNamespace mimicking datetime.datetime with ``now`` mocked.

    The returned object can be used with ``unittest.mock.patch`` or manually
    assigned to ``datetime.datetime`` in the module's globals.
    """
    class MockDateTime(datetime.datetime):
        @classmethod
        def now(cls, tz=None):  # type: ignore[override]
            return target.replace(tzinfo=tz)

    return MockDateTime


def test_render_time_known_timestamp():
    # 13:37 should render as the ASCII art for "13:37"
    dt = datetime.datetime(2023, 1, 1, 13, 37)
    expected = (
        "    _   _   .   _   _\n"
        "  | _|  _|  .  |_  |_\n"
        "  | _| |_   .   _|  _|"
    )
    # The expected string is built manually based on the digit map.
    result = render_time(dt)
    assert result == expected


def test_main_uses_mocked_now(monkeypatch, capsys):
    # Mock datetime.datetime.now to return 09:05
    mock_dt = datetime.datetime(2022, 12, 31, 9, 5)
    MockDateTime = _mock_datetime(mock_dt)
    monkeypatch.setattr('src.clock.datetime.datetime', MockDateTime)

    # Run the CLI entry point
    main([])
    captured = capsys.readouterr().out.strip()

    expected = (
        " _   _   .   _   _\n"
        "| |  _|  .  |_   _|\n"
        "|_| |_   .   _| |_ "
    )
    # Normalise whitespace for comparison
    assert captured.replace('\r', '') == expected
