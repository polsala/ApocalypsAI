import datetime
from src.tip_generator import get_tip_for_date, TIPS


def test_known_date_returns_expected_tip():
    # Mock rationale: Use a fixed date to verify deterministic selection.
    test_date = datetime.date(2023, 1, 1)  # Known ordinal: 738156
    expected_index = test_date.toordinal() % len(TIPS)
    expected_tip = TIPS[expected_index]
    assert get_tip_for_date(test_date) == expected_tip


def test_today_cli_output(monkeypatch, capsys):
    # Mock rationale: Patch datetime.date.today() to a known value.
    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return datetime.date(2025, 12, 31)

    monkeypatch.setattr(datetime, "date", MockDate)
    # Import the module after monkeypatching so main() uses the mock.
    from src import tip_generator
    tip_generator.main()
    captured = capsys.readouterr()
    expected_index = MockDate.today().toordinal() % len(TIPS)
    expected_tip = TIPS[expected_index] + "\n"
    assert captured.out == expected_tip
