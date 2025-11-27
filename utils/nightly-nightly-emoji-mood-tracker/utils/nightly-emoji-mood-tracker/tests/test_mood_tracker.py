import unittest
from unittest import mock
from pathlib import Path

# Import the module under test
from utils.nightly-emoji-mood-tracker.src import mood_tracker

# Mock rationale: All filesystem interactions are redirected to an in‑memory temporary path
# so tests remain deterministic and offline.
MOCK_STORE_PATH = Path("/tmp/mock_emoji_mood.json")


def _mock_path_exists(self):
    return MOCK_STORE_PATH.exists()


def _mock_open_read(*args, **kwargs):
    # Return an empty JSON object if the mock file does not exist yet
    if not MOCK_STORE_PATH.exists():
        return mock.mock_open(read_data="{}")(*args, **kwargs)
    return mock.mock_open(read_data=MOCK_STORE_PATH.read_text())(*args, **kwargs)


def _mock_open_write(*args, **kwargs):
    # Capture writes to the mock path
    m = mock.mock_open()
    handle = m(*args, **kwargs)
    original_write = handle.write

    def write(data):
        # Write to the in‑memory file
        MOCK_STORE_PATH.write_text(data)
        return original_write(data)

    handle.write.side_effect = write
    return m


class TestMoodTracker(unittest.TestCase):
    def setUp(self):
        # Ensure a clean mock file before each test
        if MOCK_STORE_PATH.exists():
            MOCK_STORE_PATH.unlink()

    @mock.patch.object(mood_tracker, "STORE_PATH", MOCK_STORE_PATH)
    def test_add_new_entry(self):
        created, msg = mood_tracker.add_entry("😊")
        self.assertTrue(created)
        self.assertIn("Added mood", msg)
        # Verify persistence
        with MOCK_STORE_PATH.open() as f:
            data = f.read()
        self.assertIn("\"" + mood_tracker.date.today().isoformat() + "\": \"😊\"", data)

    @mock.patch.object(mood_tracker, "STORE_PATH", MOCK_STORE_PATH)
    def test_update_existing_entry(self):
        # First add
        mood_tracker.add_entry("😊", "2025-01-01")
        # Update same date
        created, msg = mood_tracker.add_entry("😢", "2025-01-01")
        self.assertFalse(created)
        self.assertIn("Updated mood", msg)
        # Verify the value changed
        with MOCK_STORE_PATH.open() as f:
            store = json.load(f)
        self.assertEqual(store["2025-01-01"], "😢")

    @mock.patch.object(mood_tracker, "STORE_PATH", MOCK_STORE_PATH)
    def test_summary_counts(self):
        # Populate multiple entries
        mood_tracker.add_entry("😊", "2025-01-01")
        mood_tracker.add_entry("😊", "2025-01-02")
        mood_tracker.add_entry("😢", "2025-01-03")
        counts = mood_tracker.summary()
        self.assertEqual(counts, {"😊": 2, "😢": 1})

    @mock.patch.object(mood_tracker, "STORE_PATH", MOCK_STORE_PATH)
    def test_summary_empty(self):
        counts = mood_tracker.summary()
        self.assertEqual(counts, {})

    def tearDown(self):
        if MOCK_STORE_PATH.exists():
            MOCK_STORE_PATH.unlink()


if __name__ == "__main__":
    unittest.main()
