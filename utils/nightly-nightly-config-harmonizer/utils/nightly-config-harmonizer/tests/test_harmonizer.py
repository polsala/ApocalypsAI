import unittest
from unittest.mock import patch, mock_open
import sys
import os
import io
import argparse

# Mock rationale: We need to simulate file system interactions (reading YAML files)
# without actually touching the disk. `unittest.mock.patch` and `mock_open` allow
# us to control the content returned when `open()` is called, making tests deterministic
# and isolated from the file system.

# Add the src directory to the path to allow importing harmonizer.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import harmonizer
sys.path.pop(0)

class TestConfigHarmonizer(unittest.TestCase):

    def setUp(self):
        # Capture stdout and stderr for testing printed output and exit codes
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = self._stdout_capture = io.StringIO()
        sys.stderr = self._stderr_capture = io.StringIO()

    def tearDown(self):
        # Restore stdout and stderr
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

    def _run_main(self, args):
        # Helper to run the main function with mocked arguments and capture exit
        with patch('argparse.ArgumentParser.parse_args', return_value=args):
            with self.assertRaises(SystemExit) as cm:
                harmonizer.main()
            return cm.exception.code

    @patch('builtins.open', new_callable=mock_open)
    def test_no_differences(self, mock_file_open):
        # Mock rationale: Simulate two identical YAML files being read.
        golden_content = """key1: value1\nkey2: { subkey1: subvalue1 }"""
        target_content = """key1: value1\nkey2: { subkey1: subvalue1 }"""

        # Configure mock_open to return different content based on the file path
        mock_file_open.side_effect = [
            io.StringIO(golden_content), # For golden-config.yaml
            io.StringIO(target_content)  # For target-config.yaml
        ]

        args = argparse.Namespace(
            golden_config='golden-config.yaml',
            target_configs=['target-config.yaml']
        )
        exit_code = self._run_main(args)

        self.assertEqual(exit_code, 0)
        self.assertIn("No discrepancies found", self._stdout_capture.getvalue())
        self.assertIn("All target configurations perfectly match", self._stdout_capture.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    def test_missing_key_in_target(self, mock_file_open):
        # Mock rationale: Simulate a target YAML file missing a key present in the golden file.
        golden_content = """key1: value1\nkey2: value2"""
        target_content = """key1: value1"""

        mock_file_open.side_effect = [
            io.StringIO(golden_content),
            io.StringIO(target_content)
        ]

        args = argparse.Namespace(
            golden_config='golden-config.yaml',
            target_configs=['target-config.yaml']
        )
        exit_code = self._run_main(args)

        self.assertEqual(exit_code, 1)
        self.assertIn("Missing key in target at 'key2'", self._stdout_capture.getvalue())
        self.assertIn("Found 1 discrepancies", self._stdout_capture.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    def test_extra_key_in_target(self, mock_file_open):
        # Mock rationale: Simulate a target YAML file having an extra key not in the golden file.
        golden_content = """key1: value1"""
        target_content = """key1: value1\nkey2: value2"""

        mock_file_open.side_effect = [
            io.StringIO(golden_content),
            io.StringIO(target_content)
        ]

        args = argparse.Namespace(
            golden_config='golden-config.yaml',
            target_configs=['target-config.yaml']
        )
        exit_code = self._run_main(args)

        self.assertEqual(exit_code, 1)
        self.assertIn("Extra key in target at 'key2': 'value2'", self._stdout_capture.getvalue())
        self.assertIn("Found 1 discrepancies", self._stdout_capture.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    def test_different_value(self, mock_file_open):
        # Mock rationale: Simulate a target YAML file having a different value for a shared key.
        golden_content = """key1: value1"""
        target_content = """key1: different_value"""

        mock_file_open.side_effect = [
            io.StringIO(golden_content),
            io.StringIO(target_content)
        ]

        args = argparse.Namespace(
            golden_config='golden-config.yaml',
            target_configs=['target-config.yaml']
        )
        exit_code = self._run_main(args)

        self.assertEqual(exit_code, 1)
        self.assertIn("Difference found at 'key1': Golden='value1', Target='different_value'", self._stdout_capture.getvalue())
        self.assertIn("Found 1 discrepancies", self._stdout_capture.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    def test_nested_differences(self, mock_file_open):
        # Mock rationale: Simulate nested YAML structures with various differences.
        golden_content = """parent:\n  child1: val1\n  child2: { grand_child1: gval1, grand_child2: gval2 }\n  child3: val3"""
        target_content = """parent:\n  child1: new_val1\n  child2: { grand_child1: gval1, grand_child3: gval3 }\n  child4: val4"""

        mock_file_open.side_effect = [
            io.StringIO(golden_content),
            io.StringIO(target_content)
        ]

        args = argparse.Namespace(
            golden_config='golden-config.yaml',
            target_configs=['target-config.yaml']
        )
        exit_code = self._run_main(args)

        self.assertEqual(exit_code, 1)
        output = self._stdout_capture.getvalue()
        self.assertIn("Difference found at 'parent.child1': Golden='val1', Target='new_val1'", output)
        self.assertIn("Missing key in target at 'parent.child2.grand_child2'", output)
        self.assertIn("Missing key in target at 'parent.child3'", output)
        self.assertIn("Extra key in target at 'parent.child2.grand_child3': 'gval3'", output)
        self.assertIn("Extra key in target at 'parent.child4': 'val4'", output)
        self.assertIn("Found 5 discrepancies", output)

    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_target_configs(self, mock_file_open):
        # Mock rationale: Simulate comparing against multiple target files.
        golden_content = """key: value"""
        target1_content = """key: value"""
        target2_content = """key: different_value"""

        mock_file_open.side_effect = [
            io.StringIO(golden_content), # Golden
            io.StringIO(target1_content), # Target 1
            io.StringIO(target2_content)  # Target 2
        ]

        args = argparse.Namespace(
            golden_config='golden-config.yaml',
            target_configs=['target1.yaml', 'target2.yaml']
        )
        exit_code = self._run_main(args)

        self.assertEqual(exit_code, 1) # Because target2 has a diff
        output = self._stdout_capture.getvalue()
        self.assertIn("No discrepancies found in target1.yaml", output)
        self.assertIn("Difference found at 'key': Golden='value', Target='different_value'", output)
        self.assertIn("Found 1 discrepancies in target2.yaml", output)
        self.assertIn("Total discrepancies found across all target configurations: 1.", output)

    @patch('builtins.open', new_callable=mock_open)
    def test_golden_config_not_found(self, mock_file_open):
        # Mock rationale: Simulate the golden config file not existing.
        mock_file_open.side_effect = FileNotFoundError # Simulate golden file not found

        args = argparse.Namespace(
            golden_config='non-existent-golden.yaml',
            target_configs=['target.yaml']
        )
        exit_code = self._run_main(args)

        self.assertEqual(exit_code, 1)
        self.assertIn("Error: Golden config file not found", self._stderr_capture.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    def test_target_config_not_found(self, mock_file_open):
        # Mock rationale: Simulate a target config file not existing.
        golden_content = """key: value"""
        mock_file_open.side_effect = [
            io.StringIO(golden_content), # Golden config exists
            FileNotFoundError           # Target config does not exist
        ]

        args = argparse.Namespace(
            golden_config='golden.yaml',
            target_configs=['non-existent-target.yaml']
        )
        exit_code = self._run_main(args)

        self.assertEqual(exit_code, 1)
        self.assertIn("Error: Target config file not found", self._stderr_capture.getvalue())
        self.assertIn("Total discrepancies found across all target configurations: 1.", self._stdout_capture.getvalue()) # Counts as 1 discrepancy

    @patch('builtins.open', new_callable=mock_open)
    def test_invalid_yaml_golden(self, mock_file_open):
        # Mock rationale: Simulate an invalid YAML golden config file.
        golden_content = """key: - invalid yaml""" # Invalid YAML

        mock_file_open.side_effect = [
            io.StringIO(golden_content),
            io.StringIO("key: value") # Dummy target
        ]

        args = argparse.Namespace(
            golden_config='invalid-golden.yaml',
            target_configs=['target.yaml']
        )
        exit_code = self._run_main(args)

        self.assertEqual(exit_code, 1)
        self.assertIn("Error parsing golden config", self._stderr_capture.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    def test_invalid_yaml_target(self, mock_file_open):
        # Mock rationale: Simulate an invalid YAML target config file.
        golden_content = """key: value"""
        target_content = """key: - invalid yaml""" # Invalid YAML

        mock_file_open.side_effect = [
            io.StringIO(golden_content),
            io.StringIO(target_content)
        ]

        args = argparse.Namespace(
            golden_config='golden.yaml',
            target_configs=['invalid-target.yaml']
        )
        exit_code = self._run_main(args)

        self.assertEqual(exit_code, 1)
        self.assertIn("Error parsing target config", self._stderr_capture.getvalue())
        self.assertIn("Total discrepancies found across all target configurations: 1.", self._stdout_capture.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    def test_golden_not_dict(self, mock_file_open):
        # Mock rationale: Simulate a golden config that is valid YAML but not a dictionary (e.g., a list).
        golden_content = """- item1\n- item2""" # A YAML list

        mock_file_open.side_effect = [
            io.StringIO(golden_content),
            io.StringIO("key: value") # Dummy target
        ]

        args = argparse.Namespace(
            golden_config='list-golden.yaml',
            target_configs=['target.yaml']
        )
        exit_code = self._run_main(args)

        self.assertEqual(exit_code, 1)
        self.assertIn("Error: Golden config 'list-golden.yaml' is not a valid YAML dictionary.", self._stderr_capture.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    def test_target_not_dict(self, mock_file_open):
        # Mock rationale: Simulate a target config that is valid YAML but not a dictionary (e.g., a list).
        golden_content = """key: value"""
        target_content = """- item1\n- item2""" # A YAML list

        mock_file_open.side_effect = [
            io.StringIO(golden_content),
            io.StringIO(target_content)
        ]

        args = argparse.Namespace(
            golden_config='golden.yaml',
            target_configs=['list-target.yaml']
        )
        exit_code = self._run_main(args)

        self.assertEqual(exit_code, 1)
        self.assertIn("Error: Target config 'list-target.yaml' is not a valid YAML dictionary. Skipping.", self._stderr_capture.getvalue())
        self.assertIn("Total discrepancies found across all target configurations: 1.", self._stdout_capture.getvalue())


if __name__ == '__main__':
    unittest.main()
