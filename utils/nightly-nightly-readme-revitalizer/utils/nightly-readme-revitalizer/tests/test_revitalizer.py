import unittest
import json
from unittest.mock import patch, mock_open
import sys
import os
import io # Import io for StringIO

# Mock rationale: We need to test the `main` function's interaction with file system and stdout/stderr.
# `mock_open` simulates file reading, `patch('sys.stdout')` and `patch('sys.stderr')` capture output.
# `patch('sys.argv')` allows us to simulate command-line arguments.

# Add the src directory to the Python path to allow importing revitalizer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import revitalizer

class TestReadmeRevitalizer(unittest.TestCase):

    def test_empty_readme(self):
        readme_content = ""
        report = revitalizer.analyze_readme(readme_content)
        self.assertEqual(report["status"], "NEEDS_REVITALIZATION")
        self.assertIn("Missing essential section: 'Installation'", report["issues"])
        self.assertIn("Missing essential section: 'Usage'", report["issues"])

    def test_readme_with_all_sections_and_no_issues(self):
        readme_content = """
# My Awesome Project

## Features
- Feature 1
- Feature 2

## Installation
```bash
npm install
```

## Usage
```python
print('Hello')
```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
MIT License. See [LICENSE](#license-details).

### License Details
Full license text here.
"""
        report = revitalizer.analyze_readme(readme_content)
        self.assertEqual(report["status"], "OK")
        self.assertEqual(len(report["issues"]), 0)

    def test_readme_with_missing_sections(self):
        readme_content = """
# My Project

## Features
- Cool stuff
"""
        report = revitalizer.analyze_readme(readme_content)
        self.assertEqual(report["status"], "NEEDS_REVITALIZATION")
        self.assertIn("Missing essential section: 'Installation'", report["issues"])
        self.assertIn("Missing essential section: 'Usage'", report["issues"])
        self.assertNotIn("Missing essential section: 'Features'", report["issues"])

    def test_readme_with_placeholder_text(self):
        readme_content = """
# YOUR_PROJECT_NAME

## Installation
TODO: Add installation steps.

## License
[LICENSE_TYPE]
"""
        report = revitalizer.analyze_readme(readme_content)
        self.assertEqual(report["status"], "NEEDS_REVITALIZATION")
        self.assertIn("Found placeholder text: 'YOUR_PROJECT_NAME'", report["issues"])
        self.assertIn("Found placeholder text: 'TODO'", report["issues"])
        self.assertIn("Found placeholder text: '[LICENSE_TYPE]'", report["issues"])

    def test_readme_with_broken_internal_link(self):
        readme_content = """
# Project

## Section A
[Link to B](#section-b)

## Section C
[Link to non-existent](#non-existent-section)
"""
        report = revitalizer.analyze_readme(readme_content)
        self.assertEqual(report["status"], "NEEDS_REVITALIZATION")
        self.assertIn("Broken internal link: '#non-existent-section' points to a non-existent section.", report["issues"])
        self.assertNotIn("Broken internal link: '#section-b'", report["issues"])

    def test_readme_with_valid_internal_links(self):
        readme_content = """
# Project Title

## Section One
Content for section one.

## Section Two
[Go to Section One](#section-one)
[Go to Section Two](#section-two)
"""
        report = revitalizer.analyze_readme(readme_content)
        self.assertEqual(report["status"], "OK")
        self.assertEqual(len(report["issues"]), 0)

    def test_readme_with_complex_heading_anchors(self):
        readme_content = """
# Project

## A Section with Spaces and - Hyphens -
[Link](#a-section-with-spaces-and---hyphens--)

## Another Section! With Punctuation?
[Link](#another-section-with-punctuation)
"""
        report = revitalizer.analyze_readme(readme_content)
        self.assertEqual(report["status"], "OK")
        self.assertEqual(len(report["issues"]), 0)

    @patch('builtins.open', new_callable=mock_open, read_data="# Test\n## Installation")
    @patch('sys.stdout', new_callable=io.StringIO) # Mock rationale: Capture stdout to verify JSON output.
    @patch('sys.argv', ['revitalizer.py', 'dummy_path/README.md'])
    def test_main_function_with_file_path(self, mock_argv, mock_stdout, mock_open_file):
        # Mock rationale: Simulates `python src/revitalizer.py path/to/file.md`.
        # `mock_open` provides the file content, `sys.stdout` is mocked to capture output.
        revitalizer.main()
        mock_open_file.assert_called_once_with('dummy_path/README.md', 'r', encoding='utf-8')
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(output["status"], "NEEDS_REVITALIZATION")
        self.assertIn("Missing essential section: 'Usage'", output["issues"])

    @patch('sys.stdin', new_callable=lambda: io.StringIO("# Test\n## Usage"))
    @patch('sys.stdout', new_callable=io.StringIO) # Mock rationale: Capture stdout to verify JSON output.
    @patch('sys.argv', ['revitalizer.py'])
    def test_main_function_with_stdin(self, mock_argv, mock_stdout, mock_stdin):
        # Mock rationale: Simulates `cat file.md | python src/revitalizer.py`.
        # `sys.stdin` is mocked to provide input, `sys.stdout` is mocked to capture output.
        revitalizer.main()
        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(output["status"], "NEEDS_REVITALIZATION")
        self.assertIn("Missing essential section: 'Installation'", output["issues"])

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.stdout', new_callable=io.StringIO) # Mock rationale: Capture stdout to prevent printing during test.
    @patch('sys.stderr', new_callable=io.StringIO) # Mock rationale: Capture stderr to verify error output.
    @patch('sys.argv', ['revitalizer.py', 'non_existent_file.md'])
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_function_file_not_found(self, mock_exit, mock_stderr, mock_stdout, mock_open_file):
        # Mock rationale: Simulates `python src/revitalizer.py non_existent.md` where file is not found.
        # `mock_open` raises FileNotFoundError, `sys.stderr` captures error output, `sys.exit` is mocked to prevent actual exit.
        revitalizer.main()
        mock_exit.assert_called_once_with(1)
        error_output = json.loads(mock_stderr.getvalue())
        self.assertEqual(error_output["status"], "ERROR")
        self.assertIn("File not found", error_output["message"])

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=io.StringIO) # Mock rationale: Capture stdout to prevent printing during test.
    @patch('sys.stderr', new_callable=io.StringIO) # Mock rationale: Capture stderr to verify error output.
    @patch('sys.argv', ['revitalizer.py', 'dummy_path/README.md'])
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_function_general_file_error(self, mock_exit, mock_stderr, mock_stdout, mock_open_file):
        # Mock rationale: Simulates a general error during file reading.
        # `mock_open` is configured to raise an arbitrary exception.
        mock_open_file.side_effect = Exception("Permission denied")
        revitalizer.main()
        mock_exit.assert_called_once_with(1)
        error_output = json.loads(mock_stderr.getvalue())
        self.assertEqual(error_output["status"], "ERROR")
        self.assertIn("Error reading file: Permission denied", error_output["message"])
