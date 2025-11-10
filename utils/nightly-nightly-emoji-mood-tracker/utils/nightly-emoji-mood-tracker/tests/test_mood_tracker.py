import json
import os
import sys
import tempfile
from datetime import date
from pathlib import Path

# Ensure the src directory is on the import path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

# Mock rationale: we fix the date to ensure deterministic behavior without network.
from mood_tracker import add_mood, get_summary

def test_add_and_summary():
    with tempfile.TemporaryDirectory() as td:
        log_path = os.path.join(td, "mood_log.json")
        fixed_date = date(2023, 1, 1)

        # Add emojis
        add_mood("😊", log_path=log_path, today=fixed_date)
        add_mood("😢", log_path=log_path, today=fixed_date)
        add_mood("😊", log_path=log_path, today=fixed_date)

        # Verify file content
        with open(log_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data == {"2023-01-01": ["😊", "😢", "😊"]}

        # Summary should count correctly
        summary = get_summary(log_path)
        assert summary["😊"] == 2
        assert summary["😢"] == 1
