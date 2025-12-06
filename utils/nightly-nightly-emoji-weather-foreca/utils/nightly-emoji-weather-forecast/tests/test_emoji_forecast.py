import importlib.util
from pathlib import Path
import pytest


def _load_module():
    """Load the emoji_forecast module without relying on package imports.

    # Mock rationale: deterministic loading from file system; no external dependencies.
    """
    module_path = Path(__file__).resolve().parents[2] / "src" / "emoji_forecast.py"
    spec = importlib.util.spec_from_file_location("emoji_forecast", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)  # type: ignore
    return module


@pytest.mark.parametrize(
    "input_desc,expected",
    [
        ("Sunny", "☀️"),
        ("clear skies", "☀️"),
        ("Partly Cloudy", "🌤️"),
        ("heavy rain", "🌧️"),
        ("light drizzle", "🌧️"),
        ("Thunderstorm", "⛈️"),
        ("snow", "❄️"),
        ("foggy morning", "🌫️"),
        ("unknown weather", "❓"),
    ],
)
def test_forecast_to_emoji(input_desc, expected):
    mod = _load_module()
    assert mod.forecast_to_emoji(input_desc) == expected
