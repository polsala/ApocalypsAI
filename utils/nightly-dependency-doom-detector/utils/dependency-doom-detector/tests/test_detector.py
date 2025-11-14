import unittest
from unittest.mock import patch, mock_open
import sys
import io
from src.detector import DependencyDoomDetector, ANCIENT_CURSE_DEPS, SHADOWY_VULNERABILITY_DEPS

class TestDependencyDoomDetector(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing printed reports
        self._original_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        # Restore original stdout
        sys.stdout = self._original_stdout

    def get_stdout(self):
        return sys.stdout.getvalue()

    @patch('builtins.open', new_callable=mock_open, read_data='[project]\nname = "test-project"\nversion = "0.1.0"\ndependencies = ["requests==2.28.1", "pyyaml>=6.0", "rich~=12.0.0"]')
    def test_no_doom_dependencies(self, mock_file):
        # Mock rationale: Simulates a pyproject.toml file with no 'doomed' dependencies
        # according to the hardcoded rules. This ensures the detector correctly identifies
        # a clean state.
        detector = DependencyDoomDetector("mock_pyproject.toml")
        detector.run()
        output = self.get_stdout()

        self.assertIn("## All Clear!", output)
        self.assertIn("requests==2.28.1", output)
        self.assertIn("pyyaml>=6.0", output)
        self.assertIn("rich~=12.0.0", output)
        self.assertEqual(len(detector.doomed_dependencies), 0)
        self.assertEqual(len(detector.clean_dependencies), 3)

    @patch('builtins.open', new_callable=mock_open, read_data='[project]\nname = "test-project"\nversion = "0.1.0"\ndependencies = ["package-a==1.0.0", "pyyaml>=6.0"]')
    def test_fragile_foundation_doom(self, mock_file):
        # Mock rationale: Simulates a pyproject.toml with a dependency pinned to an exact version.
        # This tests the 'Fragile Foundation' rule for exact version pinning.
        detector = DependencyDoomDetector("mock_pyproject.toml")
        detector.run()
        output = self.get_stdout()

        self.assertIn("## Detected Doomsayers:", output)
        self.assertIn("**package-a==1.0.0**", output)
        self.assertIn("Doom Type: Fragile Foundation", output)
        self.assertIn("Pinned to an exact version", output)
        self.assertEqual(len(detector.doomed_dependencies), 1)
        self.assertEqual(len(detector.clean_dependencies), 1)

    @patch('builtins.open', new_callable=mock_open, read_data='[project]\nname = "test-project"\nversion = "0.1.0"\ndependencies = ["ancient-lib>=0.5.0", "requests==2.28.1"]')
    def test_ancient_curse_doom(self, mock_file):
        # Mock rationale: Simulates a pyproject.toml with a dependency known to be ancient.
        # This tests the 'Ancient Curse' rule using the mocked ANCIENT_CURSE_DEPS.
        detector = DependencyDoomDetector("mock_pyproject.toml")
        detector.run()
        output = self.get_stdout()

        self.assertIn("## Detected Doomsayers:", output)
        self.assertIn("**ancient-lib>=0.5.0**", output)
        self.assertIn("Doom Type: Ancient Curse", output)
        self.assertIn("known to be extremely old", output)
        self.assertEqual(len(detector.doomed_dependencies), 1)
        self.assertEqual(len(detector.clean_dependencies), 1)

    @patch('builtins.open', new_callable=mock_open, read_data='[project]\nname = "test-project"\nversion = "0.1.0"\ndependencies = ["vulnerable-dep==2.1.0", "pyyaml>=6.0"]')
    def test_shadowy_vulnerability_doom(self, mock_file):
        # Mock rationale: Simulates a pyproject.toml with a dependency at a known vulnerable version.
        # This tests the 'Shadowy Vulnerability' rule using the mocked SHADOWY_VULNERABILITY_DEPS.
        detector = DependencyDoomDetector("mock_pyproject.toml")
        detector.run()
        output = self.get_stdout()

        self.assertIn("## Detected Doomsayers:", output)
        self.assertIn("**vulnerable-dep==2.1.0**", output)
        self.assertIn("Doom Type: Shadowy Vulnerability", output)
        self.assertIn("known (mocked) security flaw", output)
        self.assertEqual(len(detector.doomed_dependencies), 1)
        self.assertEqual(len(detector.clean_dependencies), 1)

    @patch('builtins.open', new_callable=mock_open, read_data='[project]\nname = "test-project"\nversion = "0.1.0"\ndependencies = ["package-a==1.0.0", "ancient-lib>=0.5.0", "vulnerable-dep==2.1.0", "requests>=2.0.0"]')
    def test_multiple_dooms(self, mock_file):
        # Mock rationale: Simulates a pyproject.toml with multiple types of 'doomed' dependencies.
        # This verifies that all doom detection rules are applied and reported correctly.
        detector = DependencyDoomDetector("mock_pyproject.toml")
        detector.run()
        output = self.get_stdout()

        self.assertIn("**package-a==1.0.0**", output)
        self.assertIn("Fragile Foundation", output)
        self.assertIn("**ancient-lib>=0.5.0**", output)
        self.assertIn("Ancient Curse", output)
        self.assertIn("**vulnerable-dep==2.1.0**", output)
        self.assertIn("Shadowy Vulnerability", output)
        self.assertEqual(len(detector.doomed_dependencies), 3)
        self.assertEqual(len(detector.clean_dependencies), 1)

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_file):
        # Mock rationale: Simulates the scenario where the pyproject.toml file does not exist.
        # This tests the error handling for FileNotFoundError.
        with patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                detector = DependencyDoomDetector("non_existent_file.toml")
                detector.run()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: pyproject.toml not found", mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data='[project\nname = "invalid"')
    def test_invalid_toml(self, mock_file):
        # Mock rationale: Simulates a malformed pyproject.toml file that cannot be parsed.
        # This tests the error handling for TOMLDecodeError.
        with patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
            with self.assertRaises(SystemExit) as cm:
                detector = DependencyDoomDetector("invalid_pyproject.toml")
                detector.run()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error parsing pyproject.toml", mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data='[project]\nname = "no-deps"\nversion = "0.1.0"')
    def test_no_dependencies_section(self, mock_file):
        # Mock rationale: Simulates a pyproject.toml file that exists but lacks a 'dependencies' section.
        # This tests the graceful handling of missing dependency lists.
        detector = DependencyDoomDetector("no_deps.toml")
        detector.run()
        output = self.get_stdout()
        self.assertIn("No dependencies found in pyproject.toml.", output)
        self.assertEqual(len(detector.doomed_dependencies), 0)
        self.assertEqual(len(detector.clean_dependencies), 0)

if __name__ == '__main__':
    unittest.main()
