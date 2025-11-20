import unittest
from unittest.mock import patch
import datetime
from src.manifest_generator import ManifestGenerator

class TestManifestGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = ManifestGenerator()

    def test_generate_manifest_basic_needs_low_risk_enough_time(self):
        # Test case: Basic needs, low risk, plenty of time
        daily_needs = {'food': 1, 'water': 1}
        risk_tolerance = 'low'
        scavenge_hours = 5.0
        manifest = self.generator.generate_manifest(daily_needs, risk_tolerance, scavenge_hours)

        self.assertIsInstance(manifest, list)
        self.assertEqual(len(manifest), 2)
        # Items are sorted by scarcity then time_cost. Canned Goods (scarcity 2, time 0.6) and Purification Tablet (scarcity 3, time 0.2)
        # So Canned Goods should come first for food, then Purification Tablet for water.
        self.assertEqual(manifest[0], {'name': 'Canned Goods', 'category': 'Food', 'priority': 'High', 'risk': 'Low', 'time_cost': 0.6})
        self.assertEqual(manifest[1], {'name': 'Purification Tablet', 'category': 'Water', 'priority': 'High', 'risk': 'Low', 'time_cost': 0.2})

    def test_generate_manifest_high_risk_tolerance(self):
        # Test case: High risk tolerance allows more items, including high-risk ones.
        daily_needs = {'medical': 1, 'parts': 1}
        risk_tolerance = 'high'
        scavenge_hours = 3.0
        manifest = self.generator.generate_manifest(daily_needs, risk_tolerance, scavenge_hours)

        self.assertIsInstance(manifest, list)
        self.assertEqual(len(manifest), 2)
        # Circuit Board (scarcity 5, risk high) and Medical Kit (scarcity 4, risk medium)
        # Medical Kit should come first due to lower scarcity.
        self.assertEqual(manifest[0], {'name': 'Medical Kit', 'category': 'Medical', 'priority': 'High', 'risk': 'Medium', 'time_cost': 1.0})
        self.assertEqual(manifest[1], {'name': 'Circuit Board', 'category': 'Parts', 'priority': 'High', 'risk': 'High', 'time_cost': 1.5})

    def test_generate_manifest_limited_time(self):
        # Test case: Limited time should restrict items.
        daily_needs = {'food': 2, 'water': 2, 'parts': 2}
        risk_tolerance = 'low'
        scavenge_hours = 0.5 # Very limited time
        manifest = self.generator.generate_manifest(daily_needs, risk_tolerance, scavenge_hours)

        self.assertIsInstance(manifest, list)
        # Only one item (Scrap Metal or Purification Tablet) should fit within 0.5h
        # Scrap Metal (0.3h) is lower scarcity than Purification Tablet (0.2h), but P.T. is faster.
        # The sort order is scarcity then time_cost. Scrap Metal (scarcity 1, time 0.3) comes before Purification Tablet (scarcity 3, time 0.2).
        # So Scrap Metal should be picked first.
        self.assertEqual(len(manifest), 1)
        self.assertEqual(manifest[0], {'name': 'Scrap Metal', 'category': 'Parts', 'priority': 'High', 'risk': 'Low', 'time_cost': 0.3})
        total_time = sum(item['time_cost'] for item in manifest)
        self.assertLessEqual(total_time, scavenge_hours)

    def test_generate_manifest_no_needs(self):
        # Test case: No specific needs should result in an empty manifest.
        daily_needs = {}
        risk_tolerance = 'low'
        scavenge_hours = 5.0
        manifest = self.generator.generate_manifest(daily_needs, risk_tolerance, scavenge_hours)

        self.assertIsInstance(manifest, list)
        self.assertEqual(len(manifest), 0)

    def test_generate_manifest_unfulfillable_needs(self):
        # Test case: Needs that cannot be fulfilled due to risk/time.
        daily_needs = {'medical': 1}
        risk_tolerance = 'low' # Medical Kit is medium risk, Rare Herb is high risk. Neither fits 'low'.
        scavenge_hours = 1.0
        manifest = self.generator.generate_manifest(daily_needs, risk_tolerance, scavenge_hours)

        self.assertIsInstance(manifest, list)
        self.assertEqual(len(manifest), 0)

    @patch('src.manifest_generator.datetime')
    def test_main_cli_output(self, mock_datetime):
        # Mock rationale: Ensure deterministic date output for CLI tests.
        # We mock datetime.date.today() to return a fixed date.
        mock_datetime.date.today.return_value = datetime.date(2023, 10, 27)
        mock_datetime.date = datetime.date # Ensure date object is available

        # Mock rationale: Capture stdout to verify the printed output of the main function.
        # This allows us to test the user-facing CLI output without actual console interaction.
        from io import StringIO
        import sys
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        # Mock rationale: Simulate command-line arguments for argparse.
        # This allows testing the main function's argument parsing and logic without running a subprocess.
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
            mock_parse_args.return_value = type('Args', (object,), {
                'food': 1, 'water': 1, 'parts': 0, 'medical': 0, 'tools': 0, 'morale': 0,
                'risk': 'low', 'hours': 2.0
            })()

            from src.manifest_generator import main
            main()

            output = sys.stdout.getvalue()
            sys.stdout = original_stdout # Restore stdout

            self.assertIn("--- Scavenging Manifest for 2023-10-27 ---", output)
            self.assertIn("Prioritized Needs:", output)
            self.assertIn("- Food: 1 units", output)
            self.assertIn("- Water: 1 units", output)
            self.assertIn("Risk Tolerance: Low", output)
            self.assertIn("Time Available: 2.0 hours", output)
            self.assertIn("1. Canned Goods (Food) - Priority: High, Risk: Low, Time: 0.6h", output)
            self.assertIn("2. Purification Tablet (Water) - Priority: High, Risk: Low, Time: 0.2h", output)
            self.assertIn("Total Estimated Time: 0.8 hours", output)
            self.assertIn("Good luck, survivor!", output)

    @patch('src.manifest_generator.datetime')
    def test_main_cli_output_no_items_found(self, mock_datetime):
        # Mock rationale: Ensure deterministic date output for CLI tests.
        mock_datetime.date.today.return_value = datetime.date(2023, 10, 27)
        mock_datetime.date = datetime.date

        from io import StringIO
        import sys
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
            mock_parse_args.return_value = type('Args', (object,), {
                'food': 1, 'water': 1, 'parts': 0, 'medical': 0, 'tools': 0, 'morale': 0,
                'risk': 'high', 'hours': 0.1 # Not enough time for anything
            })()

            from src.manifest_generator import main
            main()

            output = sys.stdout.getvalue()
            sys.stdout = original_stdout

            self.assertIn("No items found matching your criteria. Perhaps adjust needs, risk, or time?", output)

    @patch('src.manifest_generator.datetime')
    def test_main_cli_output_no_needs_defined(self, mock_datetime):
        # Mock rationale: Ensure deterministic date output for CLI tests.
        mock_datetime.date.today.return_value = datetime.date(2023, 10, 27)
        mock_datetime.date = datetime.date

        from io import StringIO
        import sys
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
            mock_parse_args.return_value = type('Args', (object,), {
                'food': 0, 'water': 0, 'parts': 0, 'medical': 0, 'tools': 0, 'morale': 0,
                'risk': 'low', 'hours': 5.0
            })()

            from src.manifest_generator import main
            main()

            output = sys.stdout.getvalue()
            sys.stdout = original_stdout

            self.assertIn("Prioritized Needs:\n- No specific needs defined.", output)
            self.assertIn("No items found matching your criteria. Perhaps adjust needs, risk, or time?", output)
