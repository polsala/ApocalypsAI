import unittest
import datetime
import os
import tempfile
from pathlib import Path
from io import StringIO
import sys

# Import the functions from the utility package.
# The relative import works because tests are executed with the utils folder on sys.path.
from src.mood_tracker import add_entry, load_db, show_stats

class TestMoodTracker(unittest.TestCase):
    def setUp(self):
        # Create a temporary file to act as the JSON DB.
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = Path(self.tmp.name)
        self.tmp.close()

    def tearDown(self):
        # Clean up the temporary file.
        try:
            os.unlink(self.db_path)
        except OSError:
            pass

    def test_add_and_load_entry(self):
        """Add an entry and verify it is persisted correctly."""
        add_entry("😊", "Feeling great", self.db_path)
        data = load_db(self.db_path)
        today = datetime.date.today().isoformat()
        self.assertIn(today, data)
        self.assertEqual(data[today]["mood"], "😊")
        self.assertEqual(data[today]["note"], "Feeling great")

    def test_stats_output(self):
        """Populate multiple entries and capture the stats output."""
        add_entry("😊", "", self.db_path)
        add_entry("😢", "", self.db_path)
        # Capture stdout.
        captured = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured
        try:
            show_stats(self.db_path)
        finally:
            sys.stdout = original_stdout
        output = captured.getvalue()
        # Mock rationale: we only assert that both emojis appear in the output.
        self.assertIn("😊:", output)
        self.assertIn("😢:", output)
        self.assertIn("Total days logged", output)

if __name__ == "__main__":
    unittest.main()
