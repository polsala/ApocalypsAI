import unittest
import sys
import io
from unittest.mock import patch

# Mock rationale: We need to test the script's output to stdout and its argument parsing.
# patch('sys.stdout', new_callable=io.StringIO) allows capturing print() output.
# patch('sys.argv') allows simulating command-line arguments without actually running the script via CLI.

# Import the function directly for unit testing, and the main for integration-like testing
from src.recipe_book import generate_readme, main

class TestReadmeRecipeBook(unittest.TestCase):

    def test_generate_readme_basic(self):
        project_name = "Test Project"
        sections = [] # Should trigger default sections
        readme = generate_readme(project_name, sections)

        self.assertIn(f"# {project_name}", readme)
        self.assertIn("## Overview", readme)
        self.assertIn("## Features", readme)
        self.assertIn("## Installation", readme)
        self.assertIn("## Usage", readme)
        self.assertIn("## Contributing", readme)
        self.assertIn("## License", readme)
        self.assertNotIn("## Configuration", readme)
        self.assertNotIn("## API Reference", readme)

    def test_generate_readme_specific_sections(self):
        project_name = "API Service"
        sections = ["overview", "api", "license"]
        readme = generate_readme(project_name, sections)

        self.assertIn(f"# {project_name}", readme)
        self.assertIn("## Overview", readme)
        self.assertIn("## API Reference", readme)
        self.assertIn("## License", readme)
        self.assertNotIn("## Features", readme)
        self.assertNotIn("## Installation", readme)

    def test_generate_readme_all_sections(self):
        project_name = "Full Documentation"
        sections = ["all"]
        readme = generate_readme(project_name, sections)

        # Check for a comprehensive set of sections (based on all_section_templates keys)
        expected_sections = [
            "Overview", "Features", "Installation", "Usage",
            "Configuration", "API Reference", "Contributing",
            "License", "Acknowledgements", "Roadmap"
        ]
        for section in expected_sections:
            self.assertIn(f"## {section}", readme)

    def test_generate_readme_unknown_section(self):
        project_name = "Unknown Section Test"
        sections = ["overview", "nonexistent_section", "license"]
        readme = generate_readme(project_name, sections)

        self.assertIn(f"# {project_name}", readme)
        self.assertIn("## Overview", readme)
        self.assertIn("## License", readme)
        # Check that the unknown section is still included as a placeholder
        self.assertIn("## Nonexistent Section", readme)
        self.assertIn("[Content for Nonexistent Section section]", readme)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['src/recipe_book.py', '--project-name', 'CLI Test Project'])
    def test_main_default_sections(self, mock_stdout):
        main()
        output = mock_stdout.getvalue()

        self.assertIn("# CLI Test Project", output)
        self.assertIn("## Overview", output)
        self.assertIn("## Features", output)
        self.assertIn("## Installation", output)
        self.assertIn("## Usage", output)
        self.assertIn("## Contributing", output)
        self.assertIn("## License", output)
        self.assertNotIn("## Configuration", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['src/recipe_book.py', '--project-name', 'CLI Specific Sections', '--sections', 'overview,roadmap'])
    def test_main_specific_sections(self, mock_stdout):
        main()
        output = mock_stdout.getvalue()

        self.assertIn("# CLI Specific Sections", output)
        self.assertIn("## Overview", output)
        self.assertIn("## Roadmap", output)
        self.assertNotIn("## Features", output)
        self.assertNotIn("## Installation", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['src/recipe_book.py', '--project-name', 'CLI All Sections', '--sections', 'all'])
    def test_main_all_sections(self, mock_stdout):
        main()
        output = mock_stdout.getvalue()

        expected_sections = [
            "Overview", "Features", "Installation", "Usage",
            "Configuration", "API Reference", "Contributing",
            "License", "Acknowledgements", "Roadmap"
        ]
        for section in expected_sections:
            self.assertIn(f"## {section}", output)

    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['src/recipe_book.py'])
    def test_main_missing_project_name(self, mock_exit, mock_stderr):
        # Mock rationale: argparse will call sys.exit(2) and print to stderr if required args are missing.
        # We mock sys.exit to prevent the test runner from exiting and sys.stderr to capture the error message.
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2)
        self.assertIn("argument --project-name is required", mock_stderr.getvalue())

if __name__ == '__main__':
    unittest.main()
