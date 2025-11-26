import unittest
from unittest.mock import patch, mock_open
import os
from ..src.revivalist import ReadmeRevivalist

class TestReadmeRevivalist(unittest.TestCase):

    def setUp(self):
        self.readme_path = "mock_README.md"

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_empty_readme(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate an empty README file.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = ""

        revivalist = ReadmeRevivalist(self.readme_path)
        report = revivalist.revive()
        self.assertIn("error", report)
        self.assertEqual(report["error"], ["README file not found or empty."])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_perfect_readme(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a README with no issues.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = """
# My Awesome Project

A brief description of my awesome project.

## Installation
```bash
pip install my-awesome-project
```

## Usage
```python
import my_awesome_project
my_awesome_project.run()
```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License
Distributed under the MIT License. See `LICENSE` for more information.
[Project Link](https://github.com/user/repo)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
"""
        revivalist = ReadmeRevivalist(self.readme_path)
        report = revivalist.revive()
        self.assertNotIn("error", report)
        self.assertFalse(report["missing_sections"])
        self.assertFalse(report["placeholders"])
        self.assertFalse(report["link_syntax_issues"])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_missing_sections(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a README missing key sections.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = """
# My Project

Just some text.
"""
        revivalist = ReadmeRevivalist(self.readme_path)
        report = revivalist.revive()
        self.assertIn("Missing or improperly formatted section: 'Installation'", report["missing_sections"])
        self.assertIn("Missing or improperly formatted section: 'Usage'", report["missing_sections"])
        self.assertIn("Missing or improperly formatted section: 'Contributing'", report["missing_sections"])
        self.assertIn("Missing or improperly formatted section: 'License'", report["missing_sections"])
        self.assertFalse(report["placeholders"])
        self.assertFalse(report["link_syntax_issues"])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_placeholders_found(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a README containing placeholder text.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = """
# YOUR_PROJECT_NAME

This is a PROJECT_DESCRIPTION.
TODO: Add more features.
FIXME: This part is broken.
"""
        revivalist = ReadmeRevivalist(self.readme_path)
        report = revivalist.revive()
        self.assertIn("Found placeholder text: 'YOUR_PROJECT_NAME'", report["placeholders"])
        self.assertIn("Found placeholder text: 'PROJECT_DESCRIPTION'", report["placeholders"])
        self.assertIn("Found placeholder text: 'TODO'", report["placeholders"])
        self.assertIn("Found placeholder text: 'FIXME'", report["placeholders"])
        self.assertFalse(report["missing_sections"])
        self.assertFalse(report["link_syntax_issues"])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_link_syntax_issues(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a README with malformed links.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = """
# Project

[Valid Link](https://example.com)
[Empty Link]()
[Link With Spaces](https://example.com/path with spaces)
![Image Link With Spaces](https://example.com/image with spaces.png)
"""
        revivalist = ReadmeRevivalist(self.readme_path)
        report = revivalist.revive()
        self.assertIn("Found a link with an empty URL: `[]()` or `![]()`", report["link_syntax_issues"])
        self.assertIn("Found a link with spaces in the URL: 'https://example.com/path with spaces'", report["link_syntax_issues"])
        self.assertIn("Found a link with spaces in the URL: 'https://example.com/image with spaces.png'", report["link_syntax_issues"])
        self.assertFalse(report["missing_sections"])
        self.assertFalse(report["placeholders"])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_mixed_issues(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate a README with a combination of issues.
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = """
# YOUR_PROJECT_NAME

TODO: Fix everything.
[Broken Link]()
"""
        revivalist = ReadmeRevivalist(self.readme_path)
        report = revivalist.revive()
        self.assertIn("Found placeholder text: 'YOUR_PROJECT_NAME'", report["placeholders"])
        self.assertIn("Found placeholder text: 'TODO'", report["placeholders"])
        self.assertIn("Found a link with an empty URL: `[]()` or `![]()`", report["link_syntax_issues"])
        self.assertIn("Missing or improperly formatted section: 'Installation'", report["missing_sections"])
        self.assertIn("Missing or improperly formatted section: 'Usage'", report["missing_sections"])
        self.assertIn("Missing or improperly formatted section: 'Contributing'", report["missing_sections"])
        self.assertIn("Missing or improperly formatted section: 'License'", report["missing_sections"])
