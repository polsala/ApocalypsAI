import unittest
from unittest.mock import patch, MagicMock
import time
from src.drone_dispatcher import generate_destination, generate_cargo, simulate_delivery, dispatch_drone

class TestDroneDispatcher(unittest.TestCase):

    @patch('random.choice')
    def test_generate_destination(self, mock_choice):
        # Mock rationale: Ensure deterministic selection for testing.
        mock_choice.return_value = "The Glowing Grotto"
        self.assertEqual(generate_destination(), "The Glowing Grotto")
        mock_choice.assert_called_once()

    @patch('random.choice')
    def test_generate_cargo(self, mock_choice):
        # Mock rationale: Ensure deterministic selection for testing.
        mock_choice.return_value = "a vintage pre-fall comic book"
        self.assertEqual(generate_cargo(), "a vintage pre-fall comic book")
        mock_choice.assert_called_once()

    @patch('random.randint')
    @patch('random.random')
    @patch('random.choice')
    def test_simulate_delivery_successful(self, mock_choice, mock_random, mock_randint):
        # Mock rationale: Force a successful delivery outcome.
        mock_random.return_value = 0.5 # Not in the 10% loss or 30% delay range
        mock_randint.side_effect = [
            90, # base_time_minutes
        ]
        outcome, total_time, delay_reason, loss_reason = simulate_delivery("Test Destination")
        self.assertEqual(outcome, "Successful")
        self.assertEqual(total_time, 90)
        self.assertIsNone(delay_reason)
        self.assertIsNone(loss_reason)
        mock_random.assert_called_once()
        mock_randint.assert_called_once_with(30, 180)

    @patch('random.randint')
    @patch('random.random')
    @patch('random.choice')
    def test_simulate_delivery_delayed(self, mock_choice, mock_random, mock_randint):
        # Mock rationale: Force a delayed delivery outcome.
        mock_random.return_value = 0.2 # In the 30% delay range (0.1 to 0.4)
        mock_randint.side_effect = [
            60,  # base_time_minutes
            120, # delay_minutes
        ]
        mock_choice.return_value = "Encountered unexpected radiation storm." # Mock delay reason
        outcome, total_time, delay_reason, loss_reason = simulate_delivery("Test Destination")
        self.assertEqual(outcome, "Delayed")
        self.assertEqual(total_time, 180) # 60 + 120
        self.assertEqual(delay_reason, "Encountered unexpected radiation storm.")
        self.assertIsNone(loss_reason)
        mock_random.assert_called_once()
        mock_randint.assert_called_with(60, 240) # Called twice, last call is this
        mock_choice.assert_called_once()

    @patch('random.randint')
    @patch('random.random')
    @patch('random.choice')
    def test_simulate_delivery_lost(self, mock_choice, mock_random, mock_randint):
        # Mock rationale: Force a lost delivery outcome.
        mock_random.return_value = 0.05 # In the 10% loss range (0.0 to 0.1)
        mock_randint.side_effect = [
            100, # base_time_minutes (not used for lost outcome, but called)
        ]
        mock_choice.return_value = "Temporal distortion swallowed the drone whole." # Mock loss reason
        outcome, total_time, delay_reason, loss_reason = simulate_delivery("Test Destination")
        self.assertEqual(outcome, "Lost")
        self.assertEqual(total_time, 100) # Base time is still returned, but not relevant for lost
        self.assertIsNone(delay_reason)
        self.assertEqual(loss_reason, "Temporal distortion swallowed the drone whole.")
        mock_random.assert_called_once()
        mock_randint.assert_called_once_with(30, 180)
        mock_choice.assert_called_once()

    @patch('src.drone_dispatcher.generate_destination')
    @patch('src.drone_dispatcher.generate_cargo')
    @patch('src.drone_dispatcher.simulate_delivery')
    @patch('time.gmtime')
    @patch('time.strftime')
    def test_dispatch_drone_successful_report(self, mock_strftime, mock_gmtime, mock_simulate_delivery, mock_generate_cargo, mock_generate_destination):
        # Mock rationale: Control all random and time-related functions for deterministic report generation.
        mock_generate_destination.return_value = "Test Destination"
        mock_generate_cargo.return_value = "Test Cargo"
        mock_simulate_delivery.return_value = ("Successful", 90, None, None)
        mock_gmtime.return_value = time.struct_time((2023, 10, 27, 10, 30, 0, 4, 300, 0))
        mock_strftime.return_value = "2023-10-27 10:30:00 UTC"

        report = dispatch_drone()
        expected_report = (
            "--- Drone Dispatch Report ---\n"
            "Dispatch Time: 2023-10-27 10:30:00 UTC\n"
            "Destination: Test Destination\n"
            "Cargo: Test Cargo\n"
            "Outcome: Successful\n"
            "Estimated Travel Time: 90 minutes\n"
            "Status: Cargo safely delivered to Test Destination!\n"
            "-----------------------------\n"
        )
        self.assertEqual(report, expected_report)
        mock_generate_destination.assert_called_once()
        mock_generate_cargo.assert_called_once()
        mock_simulate_delivery.assert_called_once_with("Test Destination")
        mock_gmtime.assert_called_once()
        mock_strftime.assert_called_once()

    @patch('src.drone_dispatcher.generate_destination')
    @patch('src.drone_dispatcher.generate_cargo')
    @patch('src.drone_dispatcher.simulate_delivery')
    @patch('time.gmtime')
    @patch('time.strftime')
    def test_dispatch_drone_delayed_report(self, mock_strftime, mock_gmtime, mock_simulate_delivery, mock_generate_cargo, mock_generate_destination):
        # Mock rationale: Control all random and time-related functions for deterministic report generation.
        mock_generate_destination.return_value = "Test Destination"
        mock_generate_cargo.return_value = "Test Cargo"
        mock_simulate_delivery.return_value = ("Delayed", 180, "Test Delay Reason", None)
        mock_gmtime.return_value = time.struct_time((2023, 10, 27, 10, 30, 0, 4, 300, 0))
        mock_strftime.return_value = "2023-10-27 10:30:00 UTC"

        report = dispatch_drone()
        expected_report = (
            "--- Drone Dispatch Report ---\n"
            "Dispatch Time: 2023-10-27 10:30:00 UTC\n"
            "Destination: Test Destination\n"
            "Cargo: Test Cargo\n"
            "Outcome: Delayed\n"
            "Estimated Travel Time (including delay): 180 minutes\n"
            "Delay Reason: Test Delay Reason\n"
            "Status: Cargo is en route, but running late.\n"
            "-----------------------------\n"
        )
        self.assertEqual(report, expected_report)

    @patch('src.drone_dispatcher.generate_destination')
    @patch('src.drone_dispatcher.generate_cargo')
    @patch('src.drone_dispatcher.simulate_delivery')
    @patch('time.gmtime')
    @patch('time.strftime')
    def test_dispatch_drone_lost_report(self, mock_strftime, mock_gmtime, mock_simulate_delivery, mock_generate_cargo, mock_generate_destination):
        # Mock rationale: Control all random and time-related functions for deterministic report generation.
        mock_generate_destination.return_value = "Test Destination"
        mock_generate_cargo.return_value = "Test Cargo"
        mock_simulate_delivery.return_value = ("Lost", 100, None, "Test Loss Reason")
        mock_gmtime.return_value = time.struct_time((2023, 10, 27, 10, 30, 0, 4, 300, 0))
        mock_strftime.return_value = "2023-10-27 10:30:00 UTC"

        report = dispatch_drone()
        expected_report = (
            "--- Drone Dispatch Report ---\n"
            "Dispatch Time: 2023-10-27 10:30:00 UTC\n"
            "Destination: Test Destination\n"
            "Cargo: Test Cargo\n"
            "Outcome: Lost\n"
            "Loss Reason: Test Loss Reason\n"
            "Status: Drone and cargo lost in transit. May the void have mercy.\n"
            "-----------------------------\n"
        )
        self.assertEqual(report, expected_report)
