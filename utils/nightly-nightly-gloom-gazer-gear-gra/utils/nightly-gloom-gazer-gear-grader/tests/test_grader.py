import unittest
import sys
from unittest.mock import patch, mock_open
from io import StringIO
from src.grader import GearGrader, main # Import main function

class TestGearGrader(unittest.TestCase):

    def setUp(self):
        self.grader = GearGrader()

    def test_grade_item_critical(self):
        # Essential item, very low condition
        self.assertEqual(self.grader.grade_item("Broken Axe", "weapon", 10), self.grader.PRIORITY_CRITICAL)
        # Essential item, very low condition
        self.assertEqual(self.grader.grade_item("Cracked Helmet", "armor", 19), self.grader.PRIORITY_CRITICAL)
        # Non-essential item, very low condition, but still falls under CRITICAL if condition < 20 and not caught by MISC
        # (This case is actually caught by MISC if type is not essential, so this test case is for essential types)
        self.assertEqual(self.grader.grade_item("Critical Tool", "tool", 15), self.grader.PRIORITY_CRITICAL)

    def test_grade_item_urgent(self):
        # Essential item, low condition
        self.assertEqual(self.grader.grade_item("Dull Knife", "weapon", 45), self.grader.PRIORITY_URGENT)
        # Essential item, low condition
        self.assertEqual(self.grader.grade_item("Worn Boots", "armor", 25), self.grader.PRIORITY_URGENT)
        # Essential item, just above critical threshold
        self.assertEqual(self.grader.grade_item("Flickering Flashlight", "tool", 20), self.grader.PRIORITY_URGENT)

    def test_grade_item_maintain(self):
        # Essential item, moderate condition
        self.assertEqual(self.grader.grade_item("Sturdy Backpack", "tool", 60), self.grader.PRIORITY_MAINTAIN)
        # Non-essential item, low condition (not critical, not urgent for non-essential)
        self.assertEqual(self.grader.grade_item("Tattered Map", "misc", 30), self.grader.PRIORITY_MAINTAIN)
        # Essential item, just above urgent threshold
        self.assertEqual(self.grader.grade_item("Repair Kit", "tool", 50), self.grader.PRIORITY_MAINTAIN)
        # Non-essential item, moderate condition
        self.assertEqual(self.grader.grade_item("Old Book", "entertainment", 70), self.grader.PRIORITY_MAINTAIN)

    def test_grade_item_good(self):
        # Essential item, good condition
        self.assertEqual(self.grader.grade_item("New Rifle", "weapon", 95), self.grader.PRIORITY_GOOD)
        # Non-essential item, good condition
        self.assertEqual(self.grader.grade_item("Fresh Water Bottle", "consumable", 100), self.grader.PRIORITY_GOOD)
        # Essential item, just above maintain threshold
        self.assertEqual(self.grader.grade_item("Working Radio", "tool", 80), self.grader.PRIORITY_GOOD)

    def test_grade_item_misc(self):
        # Non-essential item, very low condition
        self.assertEqual(self.grader.grade_item("Broken Toy", "toy", 5), self.grader.PRIORITY_MISC)
        self.assertEqual(self.grader.grade_item("Useless Rock", "decoration", 19), self.grader.PRIORITY_MISC)

    def test_process_gear_list_valid_input(self):
        gear_lines = [
            "Rusty Machete,weapon,35",
            "Makeshift Armor Vest,armor,60",
            "Water Purifier,tool,15",
            "First Aid Kit,consumable,90",
            "Broken Radio,misc,5",
            "Hunting Rifle,weapon,85",
            "Old Book,entertainment,70",
            "Flickering Flashlight,tool,20",
        ]
        graded_gear = self.grader.process_gear_list(gear_lines)

        self.assertIn(("Water Purifier", "tool", 15), graded_gear[self.grader.PRIORITY_CRITICAL])
        self.assertIn(("Rusty Machete", "weapon", 35), graded_gear[self.grader.PRIORITY_URGENT])
        self.assertIn(("Flickering Flashlight", "tool", 20), graded_gear[self.grader.PRIORITY_URGENT])
        self.assertIn(("Makeshift Armor Vest", "armor", 60), graded_gear[self.grader.PRIORITY_MAINTAIN])
        self.assertIn(("Old Book", "entertainment", 70), graded_gear[self.grader.PRIORITY_MAINTAIN])
        self.assertIn(("First Aid Kit", "consumable", 90), graded_gear[self.grader.PRIORITY_GOOD])
        self.assertIn(("Hunting Rifle", "weapon", 85), graded_gear[self.grader.PRIORITY_GOOD])
        self.assertIn(("Broken Radio", "misc", 5), graded_gear[self.grader.PRIORITY_MISC])

        self.assertEqual(len(graded_gear[self.grader.PRIORITY_CRITICAL]), 1)
        self.assertEqual(len(graded_gear[self.grader.PRIORITY_URGENT]), 2)
        self.assertEqual(len(graded_gear[self.grader.PRIORITY_MAINTAIN]), 2)
        self.assertEqual(len(graded_gear[self.grader.PRIORITY_GOOD]), 2)
        self.assertEqual(len(graded_gear[self.grader.PRIORITY_MISC]), 1)


    def test_process_gear_list_malformed_lines(self):
        gear_lines = [
            "Valid Item,type,50",
            "Malformed Line,type", # Missing condition
            "Another Malformed Line", # Too few parts
            "Too,Many,Parts,Here,10", # Too many parts
            "Invalid Score,type,abc", # Non-integer score
            "Invalid Range,type,101", # Score out of range
            "Invalid Range Neg,type,-5", # Score out of range
            "", # Empty line
            "   ", # Whitespace line
        ]
        # Mock rationale: Capture stderr output to check warnings without affecting console.
        with patch('sys.stderr', new=StringIO()) as fake_stderr:
            graded_gear = self.grader.process_gear_list(gear_lines)
            stderr_output = fake_stderr.getvalue()

            self.assertIn("Warning: Skipping malformed line: 'Malformed Line,type'. Expected 'Name,Type,Condition'.", stderr_output)
            self.assertIn("Warning: Skipping malformed line: 'Another Malformed Line'. Expected 'Name,Type,Condition'.", stderr_output)
            self.assertIn("Warning: Skipping malformed line: 'Too,Many,Parts,Here,10'. Expected 'Name,Type,Condition'.", stderr_output)
            self.assertIn("Warning: Skipping malformed line: 'Invalid Score,type,abc'. Condition score must be an integer.", stderr_output)
            self.assertIn("Warning: Skipping item 'Invalid Range' with invalid condition score: 101. Must be 0-100.", stderr_output)
            self.assertIn("Warning: Skipping item 'Invalid Range Neg' with invalid condition score: -5. Must be 0-100.", stderr_output)

            self.assertEqual(len(graded_gear[self.grader.PRIORITY_GOOD]), 0) # No good items
            self.assertEqual(len(graded_gear[self.grader.PRIORITY_MAINTAIN]), 1) # Only "Valid Item" should be processed
            self.assertIn(("Valid Item", "type", 50), graded_gear[self.grader.PRIORITY_MAINTAIN])


    def test_format_report(self):
        graded_gear = {
            self.grader.PRIORITY_CRITICAL: [("Water Purifier", "tool", 15)],
            self.grader.PRIORITY_URGENT: [("Rusty Machete", "weapon", 35)],
            self.grader.PRIORITY_MAINTAIN: [("Makeshift Armor Vest", "armor", 60)],
            self.grader.PRIORITY_GOOD: [("First Aid Kit", "consumable", 90)],
            self.grader.PRIORITY_MISC: [("Broken Radio", "misc", 5)],
        }
        report = self.grader.format_report(graded_gear)
        expected_report_parts = [
            "--- Gear Grading Report ---",
            "\nCRITICAL (Requires immediate attention!):",
            "  - Water Purifier (tool) - Condition: 15/100",
            "\nURGENT (Needs repair soon):",
            "  - Rusty Machete (weapon) - Condition: 35/100",
            "\nMAINTAIN (Keep an eye on it):",
            "  - Makeshift Armor Vest (armor) - Condition: 60/100",
            "\nGOOD (Ready for action!):",
            "  - First Aid Kit (consumable) - Condition: 90/100",
            "\nMISC (Non-essential, low priority):",
            "  - Broken Radio (misc) - Condition: 5/100",
        ]
        self.assertEqual(report, "\n".join(expected_report_parts))

    def test_main_function_success(self):
        mock_file_content = "Test Item 1,weapon,75\nTest Item 2,tool,10"
        # Mock rationale: Simulate reading from a file without actual file system access.
        with patch('builtins.open', mock_open(read_data=mock_file_content)) as m_open:
            # Mock rationale: Capture stdout to verify the report output.
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                # Mock rationale: Simulate command-line arguments by passing them to main.
                main(['grader.py', 'dummy_path/gear.txt'])
                output = fake_stdout.getvalue()
                self.assertIn("--- Gear Grading Report ---", output)
                self.assertIn("CRITICAL (Requires immediate attention!):", output)
                self.assertIn("  - Test Item 2 (tool) - Condition: 10/100", output)
                self.assertIn("MAINTAIN (Keep an eye on it):", output)
                self.assertIn("  - Test Item 1 (weapon) - Condition: 75/100", output)
            m_open.assert_called_once_with('dummy_path/gear.txt', 'r')

    def test_main_function_file_not_found(self):
        # Mock rationale: Simulate FileNotFoundError when opening a file.
        with patch('builtins.open', side_effect=FileNotFoundError) as m_open:
            # Mock rationale: Capture stderr to verify error message.
            with patch('sys.stderr', new=StringIO()) as fake_stderr:
                # Mock rationale: Capture sys.exit to prevent actual exit during test.
                with patch('sys.exit') as mock_exit:
                    main(['grader.py', 'non_existent_file.txt'])
                    self.assertIn("Error: File not found at 'non_existent_file.txt'", fake_stderr.getvalue())
                    mock_exit.assert_called_once_with(1)
            m_open.assert_called_once_with('non_existent_file.txt', 'r')

    def test_main_function_no_arguments(self):
        # Mock rationale: Capture stdout to verify usage message.
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            # Mock rationale: Capture sys.exit to prevent actual exit during test.
            with patch('sys.exit') as mock_exit:
                main(['grader.py'])
                self.assertIn("Usage: python src/grader.py <gear_file.txt>", fake_stdout.getvalue())
                mock_exit.assert_called_once_with(1)
