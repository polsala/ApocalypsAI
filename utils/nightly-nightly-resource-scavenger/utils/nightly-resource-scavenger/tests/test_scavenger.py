import unittest
from unittest.mock import patch, MagicMock
import os
from pathlib import Path
import sys

# Add the src directory to the Python path for importing scavenger
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
import scavenger

class TestScavenger(unittest.TestCase):

    @patch('scavenger.requests.head')
    def test_check_external_link_success(self, mock_head):
        # Mock rationale: Simulate a successful HTTP HEAD request to an external URL (status 200).
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response
        self.assertTrue(scavenger.check_external_link('http://valid.com'))

    @patch('scavenger.requests.head')
    def test_check_external_link_failure_404(self, mock_head):
        # Mock rationale: Simulate a 404 Not Found response for an external URL.
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_head.return_value = mock_response
        self.assertFalse(scavenger.check_external_link('http://broken.com'))

    @patch('scavenger.requests.head')
    def test_check_external_link_failure_exception(self, mock_head):
        # Mock rationale: Simulate a network error (e.g., connection refused, timeout) during HTTP request.
        mock_head.side_effect = scavenger.requests.exceptions.RequestException
        self.assertFalse(scavenger.check_external_link('http://unreachable.com'))

    @patch('scavenger.Path.exists')
    @patch('scavenger.Path.resolve')
    def test_check_internal_link_success(self, mock_resolve, mock_exists):
        # Mock rationale: Simulate an existing internal file path by making Path.exists() return True.
        mock_path_obj = MagicMock()
        mock_path_obj.exists.return_value = True
        mock_resolve.return_value = mock_path_obj
        
        base_path = Path('/repo/docs/current.md')
        self.assertTrue(scavenger.check_internal_link(base_path, '../another.md'))
        mock_resolve.assert_called_once() # Ensure resolve was called for a file path
        mock_exists.assert_called_once() # Ensure exists was called on the resolved path

    @patch('scavenger.Path.exists')
    @patch('scavenger.Path.resolve')
    def test_check_internal_link_failure(self, mock_resolve, mock_exists):
        # Mock rationale: Simulate a non-existent internal file path by making Path.exists() return False.
        mock_path_obj = MagicMock()
        mock_path_obj.exists.return_value = False
        mock_resolve.return_value = mock_path_obj

        base_path = Path('/repo/docs/current.md')
        self.assertFalse(scavenger.check_internal_link(base_path, 'non-existent.md'))
        mock_resolve.assert_called_once()
        mock_exists.assert_called_once()

    @patch('scavenger.Path.exists')
    @patch('scavenger.Path.resolve')
    def test_check_internal_link_anchor_only(self, mock_resolve, mock_exists):
        # Mock rationale: Pure anchor links (e.g., #section) are considered valid by the current logic.
        base_path = Path('/repo/docs/current.md')
        self.assertTrue(scavenger.check_internal_link(base_path, '#section'))
        mock_resolve.assert_not_called() # No file path to resolve for pure anchor
        mock_exists.assert_not_called() # No file existence check needed

    def test_extract_links(self):
        # Test the regex and link extraction logic with various markdown link formats.
        content = """
# Title

This is a [link to example](http://example.com).
Another link: <https://another.org/path>.
Internal link: [local file](./file.md).
Broken internal: [bad file](../nonexistent.md).
Anchor link: [go to section](#section).
"""
        expected_links = [
            ('http://example.com', 3),
            ('https://another.org/path', 4),
            ('./file.md', 5),
            ('../nonexistent.md', 6),
            ('#section', 7)
        ]
        self.assertEqual(scavenger.extract_links(content), expected_links)

    @patch('scavenger.find_markdown_files')
    @patch('scavenger.Path.read_text')
    @patch('scavenger.check_external_link')
    @patch('scavenger.check_internal_link')
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture print statements
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during test
    def test_main_no_broken_links(self, mock_exit, mock_stdout, mock_check_internal, mock_check_external, mock_read_text, mock_find_md_files):
        # Mock rationale: Simulate a scenario where all links are valid within a mock file system.
        # Mock file system to return a single markdown file.
        mock_md_file = MagicMock(spec=Path)
        mock_md_file.relative_to.return_value = Path('test.md')
        mock_find_md_files.return_value = [mock_md_file]

        # Mock file content with valid links
        mock_read_text.return_value = "[External](http://valid.com)\n[Internal](./valid.md)"

        # Mock link checkers to return True (valid) for all checks.
        mock_check_external.return_value = True
        mock_check_internal.return_value = True

        # Mock argparse to provide a path argument.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='.')):
            scavenger.main()

        mock_exit.assert_called_once_with(0) # Expect successful exit code 0
        # Verify the output message for no broken links.
        self.assertIn('Scan complete. No broken links found. All clear!', mock_stdout.call_args[0][0])

    @patch('scavenger.find_markdown_files')
    @patch('scavenger.Path.read_text')
    @patch('scavenger.check_external_link')
    @patch('scavenger.check_internal_link')
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture print statements
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during test
    def test_main_with_broken_links(self, mock_exit, mock_stdout, mock_check_internal, mock_check_external, mock_read_text, mock_find_md_files):
        # Mock rationale: Simulate a scenario with both broken external and internal links.
        # Mock file system to return a single markdown file.
        mock_md_file = MagicMock(spec=Path)
        mock_md_file.relative_to.return_value = Path('test.md')
        mock_find_md_files.return_value = [mock_md_file]

        # Mock file content with one broken external and one broken internal link.
        mock_read_text.return_value = "[Broken External](http://broken.com)\n[Broken Internal](./nonexistent.md)"

        # Mock link checkers to return False for broken links.
        mock_check_external.return_value = False
        mock_check_internal.return_value = False

        # Mock argparse to provide a path argument.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='.')):
            scavenger.main()

        mock_exit.assert_called_once_with(1) # Expect non-zero exit code 1 for broken links
        # Verify the output contains the expected broken link messages.
        output_calls = [call.args[0] for call in mock_stdout.call_args_list]
        self.assertIn('Broken Links Found:', output_calls[1])
        self.assertIn('File: test.md, Line: 1 - External: http://broken.com (Status: Unreachable)', output_calls[3])
        self.assertIn('File: test.md, Line: 2 - Internal: ./nonexistent.md (Status: File not found)', output_calls[4])
        self.assertIn('Scan complete. 2 broken links found.', output_calls[6])

    @patch('scavenger.Path.is_dir', return_value=False)
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_invalid_path(self, mock_stdout, mock_exit, mock_is_dir):
        # Mock rationale: Simulate an invalid directory path provided to the script, causing an error.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='nonexistent_dir')):
            scavenger.main()
        mock_exit.assert_called_once_with(1)
        # Verify the error message is printed to stdout.
        self.assertIn("Error: 'nonexistent_dir' is not a valid directory.", mock_stdout.call_args[0][0])

    @patch('scavenger.find_markdown_files')
    @patch('scavenger.Path.read_text', side_effect=IOError("Permission denied"))
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_file_read_error(self, mock_exit, mock_stdout, mock_read_text, mock_find_md_files):
        # Mock rationale: Simulate a file that cannot be read (e.g., permission error).
        mock_md_file = MagicMock(spec=Path)
        mock_md_file.relative_to.return_value = Path('unreadable.md')
        mock_find_md_files.return_value = [mock_md_file]

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path='.')):
            scavenger.main()
        
        mock_exit.assert_called_once_with(0) # No broken links, just a warning
        output_calls = [call.args[0] for call in mock_stdout.call_args_list]
        self.assertIn('Warning: Could not read file', output_calls[1])
        self.assertIn('Permission denied', output_calls[1])
        self.assertIn('Scan complete. No broken links found. All clear!', output_calls[2])
