import sys
from pathlib import Path
# Mock rationale: adjust import path to locate the src module without external dependencies.
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import datetime
import unittest

from zen_garden_scheduler import generate_schedule


class TestZenGardenScheduler(unittest.TestCase):
    def test_basic_schedule(self):
        """Verify schedule generation with a simple config."""
        config = {
            "activities": [
                {"name": "Meditation", "duration": 15},
                {"name": "Tea Break", "duration": 10},
                {"name": "Reading", "duration": 20},
            ]
        }
        # Mock rationale: we fix the start time to 09:00 for determinism.
        start = datetime.time(9, 0)
        expected = [
            "09:00 - 09:15: Meditation",
            "09:15 - 09:25: Tea Break",
            "09:25 - 09:45: Reading",
        ]
        result = generate_schedule(config, start_time=start)
        self.assertEqual(result, expected)

    def test_invalid_activities_type(self):
        """Ensure a non‑list activities raises ValueError."""
        config = {"activities": "not-a-list"}
        with self.assertRaises(ValueError):
            generate_schedule(config)

    def test_missing_fields(self):
        """Activities missing required fields should raise ValueError."""
        config = {"activities": [{"name": "Nap"}]}  # missing duration
        with self.assertRaises(ValueError):
            generate_schedule(config)


if __name__ == "__main__":
    unittest.main()
