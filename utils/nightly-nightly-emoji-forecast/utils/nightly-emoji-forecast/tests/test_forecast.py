import datetime
import random
import unittest
from unittest.mock import patch

# Import the module under test.
from utils.nightly-emoji-forecast.src import forecast


class TestEmojiForecast(unittest.TestCase):
    def test_deterministic_output_with_mocked_emoji_list(self):
        """# Mock rationale:
        We replace the global EMOJIS list with a tiny, predictable set so that
        the random choices are easy to reason about. The date ``2025-12-01``
        yields a known seed (20251201). Using the same seed with ``random.Random``
        we compute the expected three‑emoji string and assert equality.
        """
        mock_emojis = ["😀", "😎", "🤖", "👾"]
        test_date = datetime.date(2025, 12, 1)
        seed = int(test_date.strftime("%Y%m%d"))
        rng = random.Random(seed)
        expected = " ".join(rng.choices(mock_emojis, k=3))

        with patch.object(forecast, "EMOJIS", mock_emojis):
            result = forecast.get_forecast(test_date)
            self.assertEqual(result, expected)

    def test_cli_entry_point(self):
        """# Mock rationale:
        The CLI parses ``--date`` and prints the forecast. We patch ``sys.argv``
        to simulate a command‑line invocation and capture ``stdout``.
        """
        test_args = ["forecast.py", "--date", "2025-12-01"]
        mock_emojis = ["😀", "😎", "🤖", "👾"]
        seed = int(datetime.date(2025, 12, 1).strftime("%Y%m%d"))
        rng = random.Random(seed)
        expected_output = " ".join(rng.choices(mock_emojis, k=3))

        with patch.object(forecast, "EMOJIS", mock_emojis),
             patch.object(forecast, "__name__", "__main__"),
             patch.object(forecast, "sys") as mock_sys:
            mock_sys.argv = test_args
            # Capture stdout
            from io import StringIO
            from contextlib import redirect_stdout
            captured = StringIO()
            with redirect_stdout(captured):
                forecast.main()
            self.assertEqual(captured.getvalue().strip(), expected_output)


if __name__ == "__main__":
    unittest.main()
