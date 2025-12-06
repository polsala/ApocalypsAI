import unittest
import os
from unittest.mock import patch, mock_open
from io import StringIO
from src.duster import find_markdown_files, parse_markdown_for_links, check_links, main

class TestDigitalDustbunnyDuster(unittest.TestCase):

    @patch('os.walk')
    def test_find_markdown_files(self, mock_os_walk):
        # Mock rationale: Simulate a file system structure without actual disk I/O.
        # This ensures deterministic tests regardless of the environment.
        mock_os_walk.return_value = [
            ('/root', ('dir1', 'dir2'), ('file1.txt', 'README.md')),
            ('/root/dir1', (), ('doc.md', 'image.png')),
            ('/root/dir2', (), ('subdoc.md',)),
        ]
        
        files = find_markdown_files('/root')
        expected_files = [
            os.path.join('/root', 'README.md'),
            os.path.join('/root/dir1', 'doc.md'),
            os.path.join('/root/dir2', 'subdoc.md'),
        ]
        self.assertCountEqual(files, expected_files)

    def test_parse_markdown_for_links(self):
        content = """
        # My Document

        This is a link to [another doc](docs/chapter1.md).
        And another to [a sub-doc](../sub/chapter2.md).
        An external link: [Google](https://www.google.com).
        An anchor link: [Section](#section-heading).
        A link with spaces: [spaced link](path%20with%20spaces.md)
        A broken link: [missing](nonexistent.md)
        """
        links = parse_markdown_for_links(content)
        expected_links = [
            'docs/chapter1.md',
            '../sub/chapter2.md',
            'path%20with%20spaces.md',
            'nonexistent.md'
        ]
        self.assertCountEqual(links, expected_links)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_check_links_no_broken_links(self, mock_file_open, mock_os_path_exists):
        # Mock rationale: Simulate file content and existence without actual disk I/O.
        # This allows testing link resolution and existence checks deterministically.
        mock_file_open.side_effect = [
            StringIO("[Link to existing](existing.md)"),
            StringIO("Content of existing.md") # For the 'existing.md' file read
        ]
        mock_os_path_exists.side_effect = lambda path: path in {
            os.path.normpath('/root/file.md'),
            os.path.normpath('/root/existing.md')
        }

        root_dir = '/root'
        markdown_files = [os.path.normpath('/root/file.md')]
        
        broken_links = check_links(root_dir, markdown_files)
        self.assertEqual(broken_links, [])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_check_links_with_broken_links(self, mock_file_open, mock_os_path_exists):
        # Mock rationale: Simulate file content and existence without actual disk I/O.
        # This allows testing link resolution and existence checks deterministically.
        mock_file_open.side_effect = [
            StringIO("[Link to existing](existing.md)\n[Link to missing](missing.md)"),
            StringIO("Content of existing.md") # For the 'existing.md' file read
        ]
        mock_os_path_exists.side_effect = lambda path: path in {
            os.path.normpath('/root/file.md'),
            os.path.normpath('/root/existing.md')
        }

        root_dir = '/root'
        markdown_files = [os.path.normpath('/root/file.md')]
        
        broken_links = check_links(root_dir, markdown_files)
        expected_broken_links = [
            (os.path.normpath('/root/file.md'), 'Link to missing', os.path.normpath('/root/missing.md'))
        ]
        self.assertEqual(broken_links, expected_broken_links)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_check_links_relative_paths(self, mock_file_open, mock_os_path_exists):
        # Mock rationale: Simulate file content and existence without actual disk I/O.
        # This allows testing link resolution and existence checks for relative paths.
        mock_file_open.side_effect = [
            StringIO("[Link to sub](sub/subdoc.md)\n[Link to parent](../parentdoc.md)"),
            StringIO("Content of subdoc.md") # For the 'sub/subdoc.md' file read
        ]
        mock_os_path_exists.side_effect = lambda path: path in {
            os.path.normpath('/root/dir/file.md'),
            os.path.normpath('/root/dir/sub/subdoc.md')
        }

        root_dir = '/root'
        markdown_files = [os.path.normpath('/root/dir/file.md')]
        
        broken_links = check_links(root_dir, markdown_files)
        expected_broken_links = [
            (os.path.normpath('/root/dir/file.md'), 'Link to parent', os.path.normpath('/root/parentdoc.md'))
        ]
        self.assertEqual(broken_links, expected_broken_links)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir')
    @patch('src.duster.find_markdown_files')
    @patch('src.duster.check_links')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_markdown_files(self, mock_stdout, mock_check_links, mock_find_markdown_files, mock_os_path_isdir, mock_parse_args):
        # Mock rationale: Simulate command-line arguments, file system checks,
        # and the core logic functions to test the main execution flow without side effects.
        mock_parse_args.return_value.path = '/test/dir'
        mock_os_path_isdir.return_value = True
        mock_find_markdown_files.return_value = []
        
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("No Markdown files found to scan.", mock_stdout.getvalue())

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir')
    @patch('src.duster.find_markdown_files')
    @patch('src.duster.check_links')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_broken_links(self, mock_stdout, mock_check_links, mock_find_markdown_files, mock_os_path_isdir, mock_parse_args):
        # Mock rationale: Simulate command-line arguments, file system checks,
        # and the core logic functions to test the main execution flow without side effects.
        mock_parse_args.return_value.path = '/test/dir'
        mock_os_path_isdir.return_value = True
        mock_find_markdown_files.return_value = ['/test/dir/doc.md']
        mock_check_links.return_value = []
        
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("No digital dustbunnies (broken links) found!", mock_stdout.getvalue())

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir')
    @patch('src.duster.find_markdown_files')
    @patch('src.duster.check_links')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_broken_links(self, mock_stdout, mock_check_links, mock_find_markdown_files, mock_os_path_isdir, mock_parse_args):
        # Mock rationale: Simulate command-line arguments, file system checks,
        # and the core logic functions to test the main execution flow without side effects.
        mock_parse_args.return_value.path = '/test/dir'
        mock_os_path_isdir.return_value = True
        mock_find_markdown_files.return_value = ['/test/dir/doc.md']
        mock_check_links.return_value = [
            ('/test/dir/doc.md', 'Missing Link', os.path.normpath('/test/dir/missing.md'))
        ]
        
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1) # Expect exit code 1 for broken links
        self.assertIn("Found 1 broken links in 1 files.", mock_stdout.getvalue())
        self.assertIn("Broken link: [Missing Link]", mock_stdout.getvalue())

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_invalid_path(self, mock_stdout, mock_os_path_isdir, mock_parse_args):
        # Mock rationale: Simulate command-line arguments and file system checks
        # to test the error handling for an invalid input path.
        mock_parse_args.return_value.path = '/nonexistent/dir'
        mock_os_path_isdir.return_value = False
        
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Directory '/nonexistent/dir' not found.", mock_stdout.getvalue())
