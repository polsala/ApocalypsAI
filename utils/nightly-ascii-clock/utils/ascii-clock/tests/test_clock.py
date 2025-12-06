import unittest
import pathlib
import importlib.util
from unittest.mock import patch
import datetime

# Dynamically load the clock module without relying on package imports
MODULE_PATH = pathlib.Path(__file__).resolve().parents[2] / "src" / "clock.py"
spec = importlib.util.spec_from_file_location("clock", MODULE_PATH)
clock = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clock)

class TestAsciiClock(unittest.TestCase):
    @patch('datetime.datetime')
    def test_render_current_time_fixed(self, mock_datetime):
        # Mock rationale: ensure deterministic output without depending on the real system clock.
        fixed_dt = datetime.datetime(2023, 1, 1, 12, 34, 0)
        mock_datetime.now.return_value = fixed_dt
        # Preserve the constructor behaviour for any other datetime calls
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        expected = (
            "    _    _   \n"
            "  | _| .  _| |_|\n"
            "  | |_  .  _|  |"
        )
        self.assertEqual(clock.render_current_time(), expected)

if __name__ == "__main__":
    unittest.main()
