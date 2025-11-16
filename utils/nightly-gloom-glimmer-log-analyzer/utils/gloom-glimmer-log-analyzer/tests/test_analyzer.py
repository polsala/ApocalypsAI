import unittest
import os
import sys
import tempfile
from unittest.mock import patch, mock_open
from io import StringIO

# Adjust path to import analyzer from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from analyzer import analyze_log, load_config, DEFAULT_CONFIG, print_report

class TestGloomGlimmerLogAnalyzer(unittest.TestCase):

    def setUp(self):
        # Capture stdout for print_report tests
        self.held_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    def test_load_config_default(self):
        # Mock rationale: Test loading default configuration when no path is provided.
        # This is an internal function, no file system interaction is mocked directly,
        # but the absence of a path implicitly tests the default behavior.
        config = load_config(None)
        self.assertEqual(config, DEFAULT_CONFIG)

    def test_load_config_from_file(self):
        # Mock rationale: Test loading configuration from a specific YAML file.
        # A temporary file is used to simulate a real file on disk without
        # relying on pre-existing files or network access.
        custom_config_content = """
        patterns:
          gloom:
            - "CRITICAL_ERROR"
          glimmer:
            - "ALL_GOOD"
        """
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yaml') as tmp_file:
            tmp_file.write(custom_config_content)
            tmp_file_path = tmp_file.name

        config = load_config(tmp_file_path)
        self.assertIn("CRITICAL_ERROR", config['patterns']['gloom'])
        self.assertIn("ALL_GOOD", config['patterns']['glimmer'])
        self.assertNotIn("ERROR", config['patterns']['gloom']) # Default 'ERROR' should be overridden

        os.remove(tmp_file_path)

    def test_load_config_file_not_found(self):
        # Mock rationale: Test handling of a non-existent configuration file.
        # We pass a non-existent path and expect the default config to be loaded
        # and an error message printed to stderr.
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            config = load_config("non_existent_config.yaml")
            self.assertEqual(config, DEFAULT_CONFIG)
            self.assertIn("Error: Configuration file not found", mock_stderr.getvalue())

    def test_load_config_invalid_yaml(self):
        # Mock rationale: Test handling of an invalid YAML configuration file.
        # A temporary file with malformed YAML is created to simulate the scenario.
        invalid_config_content = """
        patterns:
          gloom:
            - "ERROR"
          glimmer: : invalid
        """
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yaml') as tmp_file:
            tmp_file.write(invalid_config_content)
            tmp_file_path = tmp_file.name

        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            config = load_config(tmp_file_path)
            self.assertEqual(config, DEFAULT_CONFIG)
            self.assertIn("Error: Invalid YAML in config file", mock_stderr.getvalue())

        os.remove(tmp_file_path)

    def test_analyze_empty_log(self):
        # Mock rationale: Test analysis of an empty log file.
        # `mock_open` is used to simulate an empty file without actual file I/O.
        with patch('builtins.open', mock_open(read_data="")) as m_open:
            results = analyze_log("empty.log", DEFAULT_CONFIG)
            self.assertEqual(results['total_lines'], 0)
            self.assertEqual(results['counts']['gloom'], 0)
            self.assertEqual(results['counts']['warning'], 0)
            self.assertEqual(results['counts']['glimmer'], 0)
            m_open.assert_called_once_with("empty.log", 'r', encoding='utf-8', errors='ignore')

    def test_analyze_log_with_gloom(self):
        # Mock rationale: Test analysis of a log file containing 'gloom' patterns.
        # `mock_open` simulates the file content.
        log_content = (
            "INFO: System started\n"
            "ERROR: Disk full\n"
            "WARNING: Low memory\n"
            "CRITICAL: Database connection lost\n"
            "DEBUG: Some debug info\n"
        )
        with patch('builtins.open', mock_open(read_data=log_content)) as m_open:
            results = analyze_log("gloom.log", DEFAULT_CONFIG)
            self.assertEqual(results['total_lines'], 5)
            self.assertEqual(results['counts']['gloom'], 2)
            self.assertEqual(results['counts']['warning'], 1)
            self.assertEqual(results['counts']['glimmer'], 0)
            self.assertIn("Line 2: ERROR: Disk full", results['gloom'])
            self.assertIn("Line 4: CRITICAL: Database connection lost", results['gloom'])
            m_open.assert_called_once_with("gloom.log", 'r', encoding='utf-8', errors='ignore')

    def test_analyze_log_with_glimmer(self):
        # Mock rationale: Test analysis of a log file containing 'glimmer' patterns.
        # `mock_open` simulates the file content.
        log_content = (
            "INFO: System started\n"
            "SUCCESS: All tests passed\n"
            "WARNING: Minor issue\n"
            "RECOVERED: Service is back online\n"
        )
        with patch('builtins.open', mock_open(read_data=log_content)) as m_open:
            results = analyze_log("glimmer.log", DEFAULT_CONFIG)
            self.assertEqual(results['total_lines'], 4)
            self.assertEqual(results['counts']['gloom'], 0)
            self.assertEqual(results['counts']['warning'], 1)
            self.assertEqual(results['counts']['glimmer'], 2)
            self.assertIn("Line 2: SUCCESS: All tests passed", results['glimmer'])
            self.assertIn("Line 4: RECOVERED: Service is back online", results['glimmer'])
            m_open.assert_called_once_with("glimmer.log", 'r', encoding='utf-8', errors='ignore')

    def test_analyze_log_case_insensitivity(self):
        # Mock rationale: Test that pattern matching is case-insensitive.
        # `mock_open` simulates the file content with mixed-case patterns.
        log_content = (
            "error: something went wrong\n"
            "WARNING: this is a warning\n"
            "Success: operation completed\n"
        )
        with patch('builtins.open', mock_open(read_data=log_content)) as m_open:
            results = analyze_log("case_insensitive.log", DEFAULT_CONFIG)
            self.assertEqual(results['total_lines'], 3)
            self.assertEqual(results['counts']['gloom'], 1)
            self.assertEqual(results['counts']['warning'], 1)
            self.assertEqual(results['counts']['glimmer'], 1)
            self.assertIn("Line 1: error: something went wrong", results['gloom'])
            self.assertIn("Line 3: Success: operation completed", results['glimmer'])
            m_open.assert_called_once_with("case_insensitive.log", 'r', encoding='utf-8', errors='ignore')

    def test_analyze_log_file_not_found(self):
        # Mock rationale: Test handling of a non-existent log file.
        # `FileNotFoundError` is explicitly raised by `mock_open` to simulate the scenario.
        with patch('builtins.open', side_effect=FileNotFoundError) as m_open, \
             patch('sys.stderr', new_callable=StringIO) as mock_stderr, \
             patch('sys.exit') as mock_exit:
            analyze_log("non_existent.log", DEFAULT_CONFIG)
            mock_exit.assert_called_once_with(1)
            self.assertIn("Error: Log file not found", mock_stderr.getvalue())
            m_open.assert_called_once_with("non_existent.log", 'r', encoding='utf-8', errors='ignore')

    def test_print_report(self):
        # Mock rationale: Test the formatting and content of the printed report.
        # `StringIO` captures stdout to verify the printed output.
        mock_results = {
            'gloom': ["  - Line 10: [ERROR] Disk full.", "  - Line 25: [CRITICAL] Core meltdown imminent."],
            'warning': [], # Warnings are not printed individually by default
            'glimmer': ["  - Line 40: [SUCCESS] Data backup complete."],
            'counts': {'gloom': 2, 'warning': 1, 'glimmer': 1},
            'total_lines': 50
        }
        log_file_path = "/path/to/test.log"

        print_report(log_file_path, mock_results)
        output = sys.stdout.getvalue()

        self.assertIn("--- Gloom-Glimmer Log Analysis Report ---", output)
        self.assertIn(f"Log File: {log_file_path}", output)
        self.assertIn("Gloom (Errors/Critical): 2", output)
        self.assertIn("  - Line 10: [ERROR] Disk full.", output)
        self.assertIn("  - Line 25: [CRITICAL] Core meltdown imminent.", output)
        self.assertIn("Warning (Warnings/Issues): 1", output)
        self.assertIn("Glimmer (Success/Hope): 1", output)
        self.assertIn("  - Line 40: [SUCCESS] Data backup complete.", output)
        self.assertIn("Total Lines Analyzed: 50", output)
        self.assertIn("--- End Report ---", output)

    def test_main_functionality(self):
        # Mock rationale: Test the end-to-end execution of the main function.
        # `patch` is used to mock `argparse` arguments, `load_config`, `analyze_log`,
        # and `print_report` to isolate the `main` function's flow. `mock_open` is used
        # to simulate the log file content if `analyze_log` were not mocked.
        log_content = "ERROR: Test error\nSUCCESS: Test success\n"
        mock_config = {'patterns': {'gloom': ['ERROR'], 'glimmer': ['SUCCESS']}}
        mock_analysis_results = {
            'gloom': ["  - Line 1: ERROR: Test error"],
            'warning': [],
            'glimmer': ["  - Line 2: SUCCESS: Test success"],
            'counts': {'gloom': 1, 'warning': 0, 'glimmer': 1},
            'total_lines': 2
        }

        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args, \
             patch('analyzer.load_config', return_value=mock_config) as mock_load_config, \
             patch('analyzer.analyze_log', return_value=mock_analysis_results) as mock_analyze_log, \
             patch('analyzer.print_report') as mock_print_report, \
             patch('builtins.open', mock_open(read_data=log_content)): # Mock open for analyze_log if it were called directly
            
            mock_parse_args.return_value.log_file_path = "mock_log.log"
            mock_parse_args.return_value.config = None

            from analyzer import main
            main()

            mock_parse_args.assert_called_once()
            mock_load_config.assert_called_once_with(None)
            mock_analyze_log.assert_called_once_with("mock_log.log", mock_config)
            mock_print_report.assert_called_once_with("mock_log.log", mock_analysis_results)


if __name__ == '__main__':
    unittest.main()
