import unittest
from unittest.mock import patch, mock_open
import os
import sys
from io import StringIO

# Import the functions from the utility script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from morale_monitor import read_events, calculate_morale, generate_report, MORALE_IMPACTS, main
sys.path.pop(0)

class TestMoraleMonitor(unittest.TestCase):

    def test_read_events_success(self):
        # Mock rationale: We need to simulate reading from a file without actually creating one.
        # `mock_open` allows us to provide a string that acts as the file content.
        mock_file_content = "found a shiny bottle cap\nran out of water\nfixed the radio\n"
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as m_open:
            events = read_events('dummy_events.txt')
            self.assertEqual(events, ['found a shiny bottle cap', 'ran out of water', 'fixed the radio'])
            m_open.assert_called_once_with('dummy_events.txt', 'r', encoding='utf-8')

    def test_read_events_empty_file(self):
        # Mock rationale: Simulate an empty events file.
        with patch('builtins.open', mock_open(read_data="")) as m_open:
            events = read_events('empty_events.txt')
            self.assertEqual(events, [])

    def test_read_events_file_not_found(self):
        # Mock rationale: Simulate the scenario where the events file does not exist.
        # `os.path.exists` is mocked to return False.
        with patch('os.path.exists', return_value=False):
            # Mock stdout to capture error messages printed by the function
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                events = read_events('non_existent.txt')
                self.assertEqual(events, [])
                self.assertIn("Error: Events file not found", fake_stdout.getvalue())

    def test_calculate_morale_positive_events(self):
        events = [
            "found a rare artifact",
            "fixed the generator",
            "shared a meal with neighbors"
        ]
        expected_morale = MORALE_IMPACTS["found"] + MORALE_IMPACTS["fixed"] + MORALE_IMPACTS["shared"]
        self.assertEqual(calculate_morale(events), expected_morale)

    def test_calculate_morale_negative_events(self):
        events = [
            "lost my favorite wrench",
            "ran out of medical supplies",
            "argued with the scavenger team"
        ]
        expected_morale = MORALE_IMPACTS["lost"] + MORALE_IMPACTS["ran out"] + MORALE_IMPACTS["argued"]
        self.assertEqual(calculate_morale(events), expected_morale)

    def test_calculate_morale_mixed_events(self):
        events = [
            "found a map",
            "broke the water filter",
            "discovered a new safe route",
            "mourned the loss of a pet"
        ]
        expected_morale = MORALE_IMPACTS["found"] + MORALE_IMPACTS["broke"] + MORALE_IMPACTS["discovered"] + MORALE_IMPACTS["mourned"]
        self.assertEqual(calculate_morale(events), expected_morale)

    def test_calculate_morale_no_impact_events(self):
        events = [
            "saw a cloud shaped like a rabbit",
            "ate some mystery meat",
            "walked for miles"
        ]
        # 'saw' has an impact, others do not
        expected_morale = MORALE_IMPACTS["saw"]
        self.assertEqual(calculate_morale(events), expected_morale)

    def test_calculate_morale_empty_list(self):
        self.assertEqual(calculate_morale([]), 0)

    def test_generate_report_radiant(self):
        report = generate_report(20)
        self.assertIn("Radiant!", report)
        self.assertIn("Total Morale Score: 20", report)

    def test_generate_report_optimistic_glow(self):
        report = generate_report(7)
        self.assertIn("Optimistic Glow.", report)
        self.assertIn("Total Morale Score: 7", report)

    def test_generate_report_holding_steady(self):
        report = generate_report(0)
        self.assertIn("Holding Steady.", report)
        self.assertIn("Total Morale Score: 0", report)

        report = generate_report(-3)
        self.assertIn("Holding Steady.", report)
        self.assertIn("Total Morale Score: -3", report)

    def test_generate_report_a_bit_grimy(self):
        report = generate_report(-10)
        self.assertIn("A Bit Grimy.", report)
        self.assertIn("Total Morale Score: -10", report)

    def test_main_functionality(self):
        # Mock rationale: Simulate the entire script execution.
        # We mock `os.path.exists` to ensure the file is 'found'.
        # We mock `builtins.open` to provide the file content.
        # We mock `sys.stdout` to capture the printed report.
        mock_file_content = (
            "found a rare book\n"
            "ran out of clean water\n"
            "fixed the communal stove\n"
            "argued over scavenging routes\n"
        )
        with patch('os.path.exists', return_value=True),
             patch('builtins.open', mock_open(read_data=mock_file_content)),
             patch('sys.stdout', new=StringIO()) as fake_stdout:
            main()
            output = fake_stdout.getvalue()
            # Expected morale: found(5) + ran out(-5) + fixed(6) + argued(-6) = 0
            self.assertIn("Holding Steady.", output)
            self.assertIn("Total Morale Score: 0", output)

    def test_main_no_events_file(self):
        # Mock rationale: Test main's behavior when the events file is not found.
        with patch('os.path.exists', return_value=False),
             patch('sys.stdout', new=StringIO()) as fake_stdout:
            main()
            output = fake_stdout.getvalue()
            self.assertIn("Error: Events file not found", output)
            self.assertIn("No events to process. Morale remains a mystery.", output)

    def test_main_empty_events_file(self):
        # Mock rationale: Test main's behavior when the events file is empty.
        with patch('os.path.exists', return_value=True),
             patch('builtins.open', mock_open(read_data="")), 
             patch('sys.stdout', new=StringIO()) as fake_stdout:
            main()
            output = fake_stdout.getvalue()
            self.assertIn("No events to process. Morale remains a mystery.", output)

if __name__ == '__main__':
    unittest.main()
