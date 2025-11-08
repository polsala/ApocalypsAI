import unittest
import sys
from unittest.mock import patch
from io import StringIO

from src.allocator import calculate_needs, main, DEFAULT_CONSUMPTION_RATES

class TestAllocator(unittest.TestCase):

    def test_calculate_needs_sufficient_resources(self):
        # Mock rationale: Testing core calculation logic with predefined inputs.
        population = 10
        duration_days = 5
        current_resources = {'food': 100, 'water': 150, 'ammo': 10, 'meds': 5}
        
        result = calculate_needs(population, duration_days, current_resources, DEFAULT_CONSUMPTION_RATES)
        
        self.assertTrue(result['possible'])
        self.assertIn('POSSIBLE', result['verdict'])
        self.assertAlmostEqual(result['details']['required']['food'], 10 * 5 * 2.0)
        self.assertAlmostEqual(result['details']['required']['water'], 10 * 5 * 3.0)
        self.assertAlmostEqual(result['details']['required']['ammo'], 10 * 5 * 0.1)
        self.assertAlmostEqual(result['details']['required']['meds'], 10 * 5 * 0.05)
        
        self.assertAlmostEqual(result['details']['remaining']['food'], 100 - (10 * 5 * 2.0))
        self.assertAlmostEqual(result['details']['remaining']['water'], 150 - (10 * 5 * 3.0))
        self.assertAlmostEqual(result['details']['remaining']['ammo'], 10 - (10 * 5 * 0.1))
        self.assertAlmostEqual(result['details']['remaining']['meds'], 5 - (10 * 5 * 0.05))
        
        self.assertIn('food', result['details']['surpluses'])
        self.assertIn('water', result['details']['surpluses'])
        self.assertIn('ammo', result['details']['surpluses'])
        self.assertIn('meds', result['details']['surpluses'])
        self.assertFalse(result['details']['shortfalls'])

    def test_calculate_needs_insufficient_resources(self):
        # Mock rationale: Testing core calculation logic with predefined inputs leading to shortfalls.
        population = 20
        duration_days = 10
        current_resources = {'food': 100, 'water': 100, 'ammo': 5, 'meds': 1}
        
        result = calculate_needs(population, duration_days, current_resources, DEFAULT_CONSUMPTION_RATES)
        
        self.assertFalse(result['possible'])
        self.assertIn('IMPOSSIBLE', result['verdict'])
        
        # Expected shortfalls:
        # Food: 20*10*2 = 400. Current 100. Shortfall = 300
        # Water: 20*10*3 = 600. Current 100. Shortfall = 500
        # Ammo: 20*10*0.1 = 20. Current 5. Shortfall = 15
        # Meds: 20*10*0.05 = 10. Current 1. Shortfall = 9
        
        self.assertAlmostEqual(result['details']['shortfalls']['food'], 300.0)
        self.assertAlmostEqual(result['details']['shortfalls']['water'], 500.0)
        self.assertAlmostEqual(result['details']['shortfalls']['ammo'], 15.0)
        self.assertAlmostEqual(result['details']['shortfalls']['meds'], 9.0)
        self.assertFalse(result['details']['surpluses'])

    def test_calculate_needs_zero_population_or_duration(self):
        # Mock rationale: Testing edge cases for population and duration.
        current_resources = {'food': 100}
        
        result_pop_zero = calculate_needs(0, 10, current_resources, DEFAULT_CONSUMPTION_RATES)
        self.assertFalse(result_pop_zero['possible'])
        self.assertIn('Cannot calculate', result_pop_zero['verdict'])

        result_dur_zero = calculate_needs(10, 0, current_resources, DEFAULT_CONSUMPTION_RATES)
        self.assertFalse(result_dur_zero['possible'])
        self.assertIn('Cannot calculate', result_dur_zero['verdict'])

        result_both_zero = calculate_needs(0, 0, current_resources, DEFAULT_CONSUMPTION_RATES)
        self.assertFalse(result_both_zero['possible'])
        self.assertIn('Cannot calculate', result_both_zero['verdict'])

    def test_calculate_needs_exact_match(self):
        # Mock rationale: Testing scenario where resources exactly match needs.
        population = 5
        duration_days = 2
        # Required: food=5*2*2=20, water=5*2*3=30, ammo=5*2*0.1=1, meds=5*2*0.05=0.5
        current_resources = {'food': 20, 'water': 30, 'ammo': 1, 'meds': 0.5}
        
        result = calculate_needs(population, duration_days, current_resources, DEFAULT_CONSUMPTION_RATES)
        
        self.assertTrue(result['possible'])
        self.assertIn('POSSIBLE', result['verdict'])
        self.assertFalse(result['details']['shortfalls'])
        self.assertFalse(result['details']['surpluses'])
        self.assertAlmostEqual(result['details']['remaining']['food'], 0.0)
        self.assertAlmostEqual(result['details']['remaining']['water'], 0.0)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', new=['allocator.py', '--population', '5', '--duration-days', '10', '--food', '100', '--water', '150', '--ammo', '10', '--meds', '5'])
    def test_main_sufficient_output_with_surpluses(self, mock_stdout):
        # Mock rationale: Testing CLI output for a sufficient resource scenario with clear surpluses.
        # Mock sys.stdout to capture print statements.
        # Mock sys.argv to simulate command-line arguments.
        main()
        output = mock_stdout.getvalue()
        self.assertIn('--- Survival Report ---', output)
        self.assertIn('Survival for 10 days with 5 survivors is POSSIBLE.', output)
        self.assertIn('Good news, commander!', output)
        self.assertIn('You have the following surpluses:', output)
        self.assertIn('Ammo: 5.00 units', output) # Required 5, Current 10, Surplus 5
        self.assertIn('Meds: 2.50 units', output) # Required 2.5, Current 5, Surplus 2.5
        self.assertNotIn('Food:', output) # No food surplus (Required 100, Current 100, Remaining 0)
        self.assertNotIn('Water:', output) # No water surplus (Required 150, Current 150, Remaining 0)
        self.assertIn('Required for survival:', output)
        self.assertIn('Current inventory:', output)
        self.assertIn('Remaining after allocation:', output)
        self.assertIn('--- End Report ---', output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', new=['allocator.py', '--population', '10', '--duration-days', '20', '--food', '100', '--water', '100', '--ammo', '1', '--meds', '0.1'])
    def test_main_insufficient_output(self, mock_stdout):
        # Mock rationale: Testing CLI output for an insufficient resource scenario.
        # Mock sys.stdout to capture print statements.
        # Mock sys.argv to simulate command-line arguments.
        main()
        output = mock_stdout.getvalue()
        self.assertIn('--- Survival Report ---', output)
        self.assertIn('Survival for 20 days with 10 survivors is IMPOSSIBLE.', output)
        self.assertIn('Warning, commander! Resource shortfalls detected.', output)
        self.assertIn('You are critically low on:', output)
        # Required: Food: 10*20*2=400. Current 100. Need 300.
        # Required: Water: 10*20*3=600. Current 100. Need 500.
        # Required: Ammo: 10*20*0.1=20. Current 1. Need 19.
        # Required: Meds: 10*20*0.05=10. Current 0.1. Need 9.9.
        self.assertIn('Food: Need 300.00 more units', output)
        self.assertIn('Water: Need 500.00 more units', output)
        self.assertIn('Ammo: Need 19.00 more units', output)
        self.assertIn('Meds: Need 9.90 more units', output)
        self.assertIn('--- Resource Breakdown ---', output)
        self.assertIn('--- End Report ---', output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', new=['allocator.py', '--population', '0', '--duration-days', '10', '--food', '100'])
    def test_main_zero_population_output(self, mock_stdout):
        # Mock rationale: Testing CLI output for zero population input.
        # Mock sys.stdout to capture print statements.
        # Mock sys.argv to simulate command-line arguments.
        main()
        output = mock_stdout.getvalue()
        self.assertIn('Cannot calculate for zero or negative population/duration.', output)
        self.assertIn('Survival for 10 days with 0 survivors is IMPOSSIBLE.', output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', new=['allocator.py', '--population', '5', '--duration-days', '0', '--food', '100'])
    def test_main_zero_duration_output(self, mock_stdout):
        # Mock rationale: Testing CLI output for zero duration input.
        # Mock sys.stdout to capture print statements.
        # Mock sys.argv to simulate command-line arguments.
        main()
        output = mock_stdout.getvalue()
        self.assertIn('Cannot calculate for zero or negative population/duration.', output)
        self.assertIn('Survival for 0 days with 5 survivors is IMPOSSIBLE.', output)
