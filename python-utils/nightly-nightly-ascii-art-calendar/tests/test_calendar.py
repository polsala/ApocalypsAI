import unittest
from datetime import datetime
from src.calendar import generate_ascii_calendar, parse_events


class TestAsciiCalendar(unittest.TestCase):
    def test_generate_basic_calendar(self):
        """Test generating a basic calendar without events."""
        result = generate_ascii_calendar(2024, 1)
        
        # Check that the result contains the header
        self.assertIn("January 2024", result)
        
        # Check that it contains day headers
        self.assertIn("Su Mo Tu We Th Fr Sa", result)
        
        # Check that it contains day 1
        self.assertIn(" 1", result)
        
        # Check that it contains day 31 (Jan 2024 ends on the 31st)
        self.assertIn("31", result)
    
    def test_generate_calendar_no_year(self):
        """Test generating a calendar without year in header."""
        result = generate_ascii_calendar(2024, 1, show_year=False)
        self.assertIn("January", result)
        self.assertNotIn("2024", result)
    
    def test_generate_calendar_with_events(self):
        """Test generating a calendar with event markers."""
        events = {
            "2024-01-01": "🎉",
            "2024-01-25": "⭐",
        }
        result = generate_ascii_calendar(2024, 1, events)
        
        # Check that events are marked
        self.assertIn("🎉", result)
        self.assertIn("⭐", result)
        
        # Verify the header is still there
        self.assertIn("January 2024", result)
    
    def test_generate_calendar_invalid_month(self):
        """Test that invalid month raises ValueError."""
        with self.assertRaises(ValueError):
            generate_ascii_calendar(2024, 13)
        
        with self.assertRaises(ValueError):
            generate_ascii_calendar(2024, 0)
    
    def test_parse_events_valid(self):
        """Test parsing valid event arguments."""
        event_args = ["2024-12-25=🎄", "2024-12-31=🎆"]
        result = parse_events(event_args)
        
        expected = {
            "2024-12-25": "🎄",
            "2024-12-31": "🎆",
        }
        self.assertEqual(result, expected)
    
    def test_parse_events_invalid_format(self):
        """Test that invalid event format raises ValueError."""
        with self.assertRaises(ValueError):
            parse_events(["2024-12-25"])
    
    def test_parse_events_invalid_date(self):
        """Test that invalid date format raises ValueError."""
        with self.assertRaises(ValueError):
            parse_events(["24-12-25=🎄"])
        
        with self.assertRaises(ValueError):
            parse_events(["2024-13-45=🎄"])
    
    def test_parse_events_empty(self):
        """Test parsing empty event list."""
        result = parse_events([])
        self.assertEqual(result, {})
    
    def test_generate_calendar_february_2024(self):
        """Test generating February 2024 calendar (leap year)."""
        result = generate_ascii_calendar(2024, 2)
        
        self.assertIn("February 2024", result)
        self.assertIn("29", result)  # 2024 is a leap year
        self.assertNotIn("30", result)
    
    def test_generate_calendar_february_2023(self):
        """Test generating February 2023 calendar (non-leap year)."""
        result = generate_ascii_calendar(2023, 2)
        
        self.assertIn("February 2023", result)
        self.assertNotIn("29", result)  # 2023 is not a leap year
        self.assertIn("28", result)
    
    def test_generate_calendar_long_marker_truncation(self):
        """Test that long markers are truncated to single character."""
        events = {
            "2024-01-01": "🎉🎊🎈",  # Multi-character marker
        }
        result = generate_ascii_calendar(2024, 1, events)
        
        # Should show only the first character
        self.assertIn("🎉", result)
        # Should not show the full marker
        self.assertNotIn("🎊", result)
    
    def test_generate_calendar_different_month_lengths(self):
        """Test calendars for months with different lengths."""
        # April has 30 days
        result_april = generate_ascii_calendar(2024, 4)
        self.assertIn("April 2024", result_april)
        self.assertIn("30", result_april)
        self.assertNotIn("31", result_april)
        
        # June has 30 days
        result_june = generate_ascii_calendar(2024, 6)
        self.assertIn("June 2024", result_june)
        self.assertIn("30", result_june)
        self.assertNotIn("31", result_june)
        
        # December has 31 days
        result_dec = generate_ascii_calendar(2024, 12)
        self.assertIn("December 2024", result_dec)
        self.assertIn("31", result_dec)


if __name__ == "__main__":
    # Mock rationale: These tests are deterministic and run entirely offline
    # No external APIs or network calls are made
    # All test data is hardcoded and self-contained
    unittest.main()
