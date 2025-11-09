import os
import sys

# Add the src directory to the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Mock rationale: No external calls; all logic is pure and deterministic.
from emoji_calendar import generate_calendar


def test_generate_calendar_november_2025():
    cal = generate_calendar(2025, 11)
    lines = cal.splitlines()
    # Header contains month and year
    assert "November 2025" in lines[0]
    # Weekday header present
    assert lines[1].strip() == "Mo Tu We Th Fr Sa Su"
    # First week should contain emojis for Saturday and Sunday
    first_week = lines[2]
    assert "🎉" in first_week, "Saturday emoji missing"
    assert "🌞" in first_week, "Sunday emoji missing"
    # Ensure a weekday number appears correctly (e.g., 3 on Monday of second week)
    second_week = lines[3]
    assert "3" in second_week.split(), "Expected day 3 in second week"
    # Ensure no numeric day appears where there should be a weekend emoji
    assert "1" not in first_week.split(), "Day number should be replaced by emoji on weekend"
