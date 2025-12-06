import unittest
import datetime
import sys
import pathlib

# Add the src directory to sys.path so we can import tip_generator
src_path = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

from tip_generator import get_tip, _TIPS

class TestTipGenerator(unittest.TestCase):
    def test_known_date(self):
        # Mock rationale: using a fixed date ensures deterministic output.
        test_date = datetime.date(2023, 1, 1)  # ordinal 738156
        tip = get_tip(test_date)
        expected_index = test_date.toordinal() % len(_TIPS)
        self.assertEqual(tip, _TIPS[expected_index])

    def test_today_default(self):
        # Mock rationale: patch datetime.date.today to return a known date.
        class MockDate(datetime.date):
            @classmethod
            def today(cls):
                return datetime.date(2022, 12, 31)

        original_date = datetime.date
        datetime.date = MockDate  # type: ignore
        try:
            tip = get_tip()
            expected_index = MockDate.today().toordinal() % len(_TIPS)
            self.assertEqual(tip, _TIPS[expected_index])
        finally:
            datetime.date = original_date

if __name__ == "__main__":
    unittest.main()
