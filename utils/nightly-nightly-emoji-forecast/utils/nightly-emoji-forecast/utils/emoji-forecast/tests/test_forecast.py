import datetime
import sys
from pathlib import Path

# Mock rationale: Adjust sys.path so the test can import the src module without installing the package.
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from forecast import generate_forecast, main


def test_generate_forecast_fixed_date():
    # Mock rationale: Use a fixed date to guarantee deterministic output.
    fixed_date = datetime.date(2023, 1, 1)
    forecast = generate_forecast(fixed_date)
    # With the seed "2023-01-01", the deterministic choice is "Sunny" (🌞) and no secondary condition.
    assert forecast == "🌞 Sunny."


def test_main_with_date_arg(capsys):
    # Mock rationale: Simulate CLI invocation with a known date.
    exit_code = main(["2023-01-01"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "🌞 Sunny."


def test_main_invalid_date(capsys):
    # Mock rationale: Ensure graceful handling of malformed input.
    exit_code = main(["invalid-date"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Invalid date format" in captured.err
