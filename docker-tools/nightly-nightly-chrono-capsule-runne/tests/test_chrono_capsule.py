import unittest
from unittest.mock import patch, MagicMock
import datetime
import time
from src.chrono_capsule import parse_drift_spec, apply_temporal_drift, run_capsule

class TestChronoCapsuleRunner(unittest.TestCase):

    def test_parse_drift_spec_valid(self):
        self.assertEqual(parse_drift_spec('+1d').days, 1)
        self.assertEqual(parse_drift_spec('-2h').hours, -2)
        self.assertEqual(parse_drift_spec('+30m').minutes, 30)
        self.assertEqual(parse_drift_spec('-15s').seconds, -15)

    def test_parse_drift_spec_invalid(self):
        with self.assertRaises(ValueError):
            parse_drift_spec('1day')
        with self.assertRaises(ValueError):
            parse_drift_spec('+1x')
        with self.assertRaises(ValueError):
            parse_drift_spec('invalid')

    def test_apply_temporal_drift_no_drift_spec(self):
        env_vars = ['VAR1=value1', 'CAPSULE_DATE=2023-01-01']
        self.assertEqual(apply_temporal_drift(env_vars, None), env_vars)
        self.assertEqual(apply_temporal_drift(env_vars, ''), env_vars)

    def test_apply_temporal_drift_capsule_date(self):
        env_vars = ['CAPSULE_DATE=2023-01-15', 'OTHER_VAR=test']
        drifted_env_vars = apply_temporal_drift(env_vars, '+5d')
        self.assertIn('CAPSULE_DATE=2023-01-20', drifted_env_vars)
        self.assertIn('OTHER_VAR=test', drifted_env_vars)

        drifted_env_vars = apply_temporal_drift(env_vars, '-10d')
        self.assertIn('CAPSULE_DATE=2023-01-05', drifted_env_vars)

    def test_apply_temporal_drift_capsule_timestamp(self):
        # Mock rationale: We need a consistent starting point for timestamp calculations.
        # Using a fixed timestamp for 'now' to ensure deterministic test results.
        # 2023-01-15 12:00:00 UTC
        initial_timestamp = 1673784000 
        env_vars = [f'CAPSULE_TIMESTAMP={initial_timestamp}', 'OTHER_VAR=test']

        # +1 hour
        drifted_env_vars = apply_temporal_drift(env_vars, '+1h')
        expected_timestamp_plus_1h = initial_timestamp + 3600
        self.assertIn(f'CAPSULE_TIMESTAMP={expected_timestamp_plus_1h}', drifted_env_vars)

        # -30 minutes
        drifted_env_vars = apply_temporal_drift(env_vars, '-30m')
        expected_timestamp_minus_30m = initial_timestamp - (30 * 60)
        self.assertIn(f'CAPSULE_TIMESTAMP={expected_timestamp_minus_30m}', drifted_env_vars)

    def test_apply_temporal_drift_invalid_formats(self):
        # Test invalid CAPSULE_DATE format
        env_vars_invalid_date = ['CAPSULE_DATE=invalid-date', 'OTHER_VAR=test']
        drifted_env_vars_invalid_date = apply_temporal_drift(env_vars_invalid_date, '+1d')
        self.assertIn('CAPSULE_DATE=invalid-date', drifted_env_vars_invalid_date)
        self.assertIn('OTHER_VAR=test', drifted_env_vars_invalid_date)

        # Test invalid CAPSULE_TIMESTAMP format
        env_vars_invalid_ts = ['CAPSULE_TIMESTAMP=not-a-number', 'OTHER_VAR=test']
        drifted_env_vars_invalid_ts = apply_temporal_drift(env_vars_invalid_ts, '+1h')
        self.assertIn('CAPSULE_TIMESTAMP=not-a-number', drifted_env_vars_invalid_ts)
        self.assertIn('OTHER_VAR=test', drifted_env_vars_invalid_ts)

        # Test valid timestamp that should drift
        initial_timestamp = 1673784000 # 2023-01-15 12:00:00 UTC
        env_vars_valid_ts = [f'CAPSULE_TIMESTAMP={initial_timestamp}']
        drifted_env_vars_valid_ts = apply_temporal_drift(env_vars_valid_ts, '+1h')
        expected_timestamp_plus_1h = initial_timestamp + 3600
        self.assertIn(f'CAPSULE_TIMESTAMP={expected_timestamp_plus_1h}', drifted_env_vars_valid_ts)

    @patch('subprocess.run')
    def test_run_capsule_no_drift(self, mock_subprocess_run):
        # Mock rationale: Avoid actual Docker execution for unit tests.
        # We simulate the expected output of a successful Docker command.
        mock_subprocess_run.return_value = MagicMock(
            stdout='Hello from capsule!', stderr='', returncode=0
        )

        image = 'test-image'
        command = 'echo "Hello"'
        env_vars = ['VAR=value']

        stdout, stderr = run_capsule(image, command, env_vars)

        mock_subprocess_run.assert_called_once_with(
            ['docker', 'run', '--rm', '-e', 'VAR=value', image, 'bash', '-c', command],
            capture_output=True, text=True, check=True
        )
        self.assertEqual(stdout, 'Hello from capsule!')
        self.assertEqual(stderr, '')

    @patch('subprocess.run')
    def test_run_capsule_with_drift(self, mock_subprocess_run):
        # Mock rationale: Avoid actual Docker execution for unit tests.
        # We simulate the expected output of a successful Docker command.
        mock_subprocess_run.return_value = MagicMock(
            stdout='Date: 2023-01-20, Timestamp: 1674216000', stderr='', returncode=0
        )

        image = 'test-image'
        command = 'echo "Date: $CAPSULE_DATE, Timestamp: $CAPSULE_TIMESTAMP"'
        # Mock rationale: Fixed current date/timestamp for deterministic drift calculation.
        # 2023-01-15, 2023-01-15 12:00:00 UTC
        env_vars = ['CAPSULE_DATE=2023-01-15', 'CAPSULE_TIMESTAMP=1673784000']
        drift_spec = '+5d'

        stdout, stderr = run_capsule(image, command, env_vars, drift_spec)

        # Expected drifted values:
        # CAPSULE_DATE: 2023-01-15 + 5 days = 2023-01-20
        # CAPSULE_TIMESTAMP: 1673784000 (2023-01-15 12:00:00) + 5 days = 1674216000 (2023-01-20 12:00:00)
        expected_env_date = 'CAPSULE_DATE=2023-01-20'
        expected_env_timestamp = 'CAPSULE_TIMESTAMP=1674216000'

        mock_subprocess_run.assert_called_once()
        args, kwargs = mock_subprocess_run.call_args
        self.assertIn('docker', args[0])
        self.assertIn('--rm', args[0])
        self.assertIn(image, args[0])
        self.assertIn('bash', args[0])
        self.assertIn('-c', args[0])
        self.assertIn(command, args[0])

        # Check if the drifted environment variables are passed correctly
        # The order of -e flags might vary, so check for presence
        self.assertIn('-e', args[0])
        self.assertIn(expected_env_date, args[0])
        self.assertIn(expected_env_timestamp, args[0])

        self.assertEqual(stdout, 'Date: 2023-01-20, Timestamp: 1674216000')
        self.assertEqual(stderr, '')

    @patch('subprocess.run')
    def test_run_capsule_error_execution(self, mock_subprocess_run):
        # Mock rationale: Simulate a Docker command failing.
        # This tests error handling and propagation.
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd='docker run ...', output='Container error', stderr='Something went wrong'
        )

        image = 'bad-image'
        command = 'exit 1'
        env_vars = []

        with self.assertRaises(subprocess.CalledProcessError):
            run_capsule(image, command, env_vars)

    @patch('subprocess.run')
    def test_run_capsule_docker_not_found(self, mock_subprocess_run):
        # Mock rationale: Simulate the 'docker' command not being found.
        # This tests the FileNotFoundError handling.
        mock_subprocess_run.side_effect = FileNotFoundError("docker not found")

        image = 'any-image'
        command = 'ls'
        env_vars = []

        with self.assertRaises(FileNotFoundError):
            run_capsule(image, command, env_vars)

if __name__ == '__main__':
    unittest.main()
