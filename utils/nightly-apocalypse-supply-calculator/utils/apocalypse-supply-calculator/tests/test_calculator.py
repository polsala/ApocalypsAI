import io
import json
import sys
import unittest
from unittest import mock

# Mock rationale: No external network calls are made; all logic is pure Python.

from utils.apocalypse-supply-calculator.src.calculator import calculate_supplies, main

class TestCalculateSupplies(unittest.TestCase):
    def test_basic_calculation(self):
        result = calculate_supplies(survivors=2, days=4)
        expected = {"water_liters": 2 * 4 * 3, "food_kcal": 2 * 4 * 2000}
        self.assertEqual(result, expected)

    def test_zero_values(self):
        self.assertEqual(calculate_supplies(0, 10), {"water_liters": 0, "food_kcal": 0})
        self.assertEqual(calculate_supplies(5, 0), {"water_liters": 0, "food_kcal": 0})

    def test_negative_input_raises(self):
        with self.assertRaises(ValueError):
            calculate_supplies(-1, 5)
        with self.assertRaises(ValueError):
            calculate_supplies(5, -3)

class TestCLI(unittest.TestCase):
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_success(self, mock_stdout):
        test_args = ['5', '2']
        with mock.patch.object(sys, 'argv', ['calculator'] + test_args):
            main()
        output = mock_stdout.getvalue().strip()
        expected_dict = {"water_liters": 5 * 2 * 3, "food_kcal": 5 * 2 * 2000}
        self.assertEqual(json.loads(output), expected_dict)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_invalid_args(self, mock_stdout):
        # Missing arguments should cause usage message and exit code 1
        test_args = []
        with mock.patch.object(sys, 'argv', ['calculator'] + test_args):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1)
        self.assertIn('Usage:', mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_non_integer(self, mock_stdout):
        test_args = ['two', '3']
        with mock.patch.object(sys, 'argv', ['calculator'] + test_args):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1)
        self.assertIn('Both survivors and days must be integers.', mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
