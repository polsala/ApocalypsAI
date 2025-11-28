import json
import os
import sys

# Mock rationale: adjust sys.path so the src module can be imported from the test location.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from forecast import format_forecast, emoji_for, load_weather

def test_emoji_for_known():
    assert emoji_for("sunny") == "🌞"
    assert emoji_for("RAINY") == "🌧️"
    assert emoji_for("unknown") == "❓"

def test_format_forecast():
    weather = {"temperature": 22, "condition": "cloudy"}
    assert format_forecast(weather) == "☁️ 22°C – Cloudy"

def test_load_weather(tmp_path):
    # Mock rationale: create a temporary JSON file to simulate real input.
    data = {"temperature": -5, "condition": "snow"}
    file_path = tmp_path / "weather.json"
    file_path.write_text(json.dumps(data))
    loaded = load_weather(str(file_path))
    assert loaded == data
