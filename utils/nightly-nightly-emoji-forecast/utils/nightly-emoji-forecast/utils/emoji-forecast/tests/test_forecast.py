import json
from pathlib import Path

# Mock rationale: we avoid any network calls and use deterministic JSON fixtures.

from emoji_forecast.src.forecast import get_emoji_forecast


def test_known_conditions():
    cases = {
        "clear": "☀️",
        "cloudy": "☁️",
        "rain": "🌧️",
        "snow": "❄️",
        "storm": "⛈️",
        "fog": "🌫️",
    }
    for condition, expected in cases.items():
        result = get_emoji_forecast({"condition": condition})
        assert result == expected, f"{condition} should map to {expected}"


def test_unknown_condition_returns_question_mark():
    result = get_emoji_forecast({"condition": "volcano"})
    assert result == "❓"


def test_missing_condition_key_returns_question_mark():
    result = get_emoji_forecast({})
    assert result == "❓"


def test_cli_with_mock_file(tmp_path, capsys):
    # Mock rationale: create a temporary JSON file with a known condition.
    mock_file = tmp_path / "weather.json"
    mock_file.write_text(json.dumps({"condition": "rain"}), encoding="utf-8")

    # Import the CLI entry point lazily to avoid side‑effects.
    from emoji_forecast.src.forecast import main

    exit_code = main([str(mock_file)])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "🌧️"
