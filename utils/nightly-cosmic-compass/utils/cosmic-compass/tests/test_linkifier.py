import unittest
import sys
import os
from unittest.mock import patch, mock_open
from io import StringIO
from src.linkifier import linkify_github_references, main

class TestLinkifier(unittest.TestCase):

    def test_local_issue_reference(self):
        text = "This fixes #123."
        repo = "owner/repo"
        expected = "This fixes [#123](https://github.com/owner/repo/issues/123)."
        self.assertEqual(linkify_github_references(text, repo), expected)

    def test_multiple_local_issue_references(self):
        text = "Fixes #1, #2, and #3."
        repo = "myorg/myrepo"
        expected = "Fixes [#1](https://github.com/myorg/myrepo/issues/1), [#2](https://github.com/myorg/myrepo/issues/2), and [#3](https://github.com/myorg/myrepo/issues/3)."
        self.assertEqual(linkify_github_references(text, repo), expected)

    def test_cross_repository_reference(self):
        text = "See also other_org/other_repo#456."
        repo = "owner/repo" # This default repo should not be used for cross-repo links
        expected = "See also [other_org/other_repo#456](https://github.com/other_org/other_repo/issues/456)."
        self.assertEqual(linkify_github_references(text, repo), expected)

    def test_mixed_references(self):
        text = "Fixes #123 and refers to another_org/another_repo#789. Also, check #456."
        repo = "myorg/myrepo"
        expected = (
            "Fixes [#123](https://github.com/myorg/myrepo/issues/123) "
            "and refers to [another_org/another_repo#789](https://github.com/another_org/another_repo/issues/789). "
            "Also, check [#456](https://github.com/myorg/myrepo/issues/456)."
        )
        self.assertEqual(linkify_github_references(text, repo), expected)

    def test_no_references(self):
        text = "This is just some plain text without any issue numbers."
        repo = "owner/repo"
        expected = text
        self.assertEqual(linkify_github_references(text, repo), expected)

    def test_numbers_not_references(self):
        text = "Version 1.2.3 released. My phone number is 555-1234."
        repo = "owner/repo"
        expected = text
        self.assertEqual(linkify_github_references(text, repo), expected)

    def test_issue_at_start_and_end(self):
        text = "#123 This is a test #456"
        repo = "owner/repo"
        expected = "[#123](https://github.com/owner/repo/issues/123) This is a test [#456](https://github.com/owner/repo/issues/456)"
        self.assertEqual(linkify_github_references(text, repo), expected)

    def test_repo_with_hyphens_and_underscores(self):
        text = "Fixes my-org_repo#123 and #456."
        repo = "my-org/my_repo"
        expected = (
            "Fixes [my-org_repo#123](https://github.com/my-org_repo/issues/123) "
            "and [#456](https://github.com/my-org/my_repo/issues/456)."
        )
        self.assertEqual(linkify_github_references(text, repo), expected)

    def test_empty_text(self):
        text = ""
        repo = "owner/repo"
        expected = ""
        self.assertEqual(linkify_github_references(text, repo), expected)

    def test_default_repo_validation(self):
        text = "Some text #123"
        with self.assertRaises(ValueError) as cm:
            linkify_github_references(text, "")
        self.assertIn("default_repo cannot be empty", str(cm.exception))

    # --- CLI Tests ---

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdin', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_stdin_to_stdout(self, mock_parse_args, mock_stdin, mock_stderr, mock_stdout):
        # Mock rationale: We need to simulate command-line arguments, standard input,
        # and capture standard output/error without actually interacting with the console.
        mock_parse_args.return_value = argparse.Namespace(
            repo="test_owner/test_repo",
            file=None,
            output=None
        )
        mock_stdin.write("This is a test for #123 and other_org/other_repo#456.")
        mock_stdin.seek(0) # Reset stdin buffer to the beginning

        main()

        expected_output = "This is a test for [#123](https://github.com/test_owner/test_repo/issues/123) and [other_org/other_repo#456](https://github.com/other_org/other_repo/issues/456).\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('builtins.open', new_callable=mock_open, read_data="File content with #100.")
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_file_to_stdout(self, mock_parse_args, mock_open_func, mock_stderr, mock_stdout):
        # Mock rationale: Simulate reading from a file and writing to stdout.
        # `mock_open` allows us to control file content without actual file I/O.
        mock_parse_args.return_value = argparse.Namespace(
            repo="file_owner/file_repo",
            file="input.txt",
            output=None
        )

        main()

        mock_open_func.assert_called_with("input.txt", 'r', encoding='utf-8')
        expected_output = "File content with [#100](https://github.com/file_owner/file_repo/issues/100).\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_stdin_to_file(self, mock_parse_args, mock_open_func, mock_stderr, mock_stdout):
        # Mock rationale: Simulate reading from stdin and writing to a file.
        # `mock_open` captures the written content.
        mock_parse_args.return_value = argparse.Namespace(
            repo="output_owner/output_repo",
            file=None,
            output="output.txt"
        )
        with patch('sys.stdin', new_callable=StringIO) as mock_stdin:
            mock_stdin.write("Input for file output #50.")
            mock_stdin.seek(0)

            main()

            mock_open_func.assert_called_with("output.txt", 'w', encoding='utf-8')
            handle = mock_open_func()
            handle.write.assert_called_once_with("Input for file output [#50](https://github.com/output_owner/output_repo/issues/50).")
            self.assertEqual(mock_stdout.getvalue(), "")
            self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('builtins.open', new_callable=mock_open, read_data="File content with #100.")
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_file_to_file(self, mock_parse_args, mock_open_func, mock_stderr, mock_stdout):
        # Mock rationale: Simulate reading from one file and writing to another.
        mock_parse_args.return_value = argparse.Namespace(
            repo="file_to_file_owner/file_to_file_repo",
            file="input.txt",
            output="output.txt"
        )

        main()

        mock_open_func.assert_any_call("input.txt", 'r', encoding='utf-8')
        mock_open_func.assert_any_call("output.txt", 'w', encoding='utf-8')
        handle = mock_open_func() # This gets the last mock_open call, which is for output.txt
        handle.write.assert_called_once_with("File content with [#100](https://github.com/file_to_file_owner/file_to_file_repo/issues/100).")
        self.assertEqual(mock_stdout.getvalue(), "")
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_no_repo_arg_or_env(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Test error handling when no repository is provided.
        mock_parse_args.return_value = argparse.Namespace(
            repo=None,
            file=None,
            output=None
        )
        # Ensure GITHUB_REPOSITORY is not set for this test
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: No default repository provided.", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_repo_from_env_var(self, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Test that the utility correctly picks up the repository from the environment variable.
        mock_parse_args.return_value = argparse.Namespace(
            repo=None,
            file=None,
            output=None
        )
        with patch.dict(os.environ, {"GITHUB_REPOSITORY": "env_owner/env_repo"}):
            with patch('sys.stdin', new_callable=StringIO) as mock_stdin:
                mock_stdin.write("Env var test #99.")
                mock_stdin.seek(0)
                main()
                expected_output = "Env var test [#99](https://github.com/env_owner/env_repo/issues/99).\n"
                self.assertEqual(mock_stdout.getvalue(), expected_output)
                self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_file_not_found(self, mock_parse_args, mock_open_func, mock_stderr, mock_stdout):
        # Mock rationale: Simulate a FileNotFoundError when trying to open the input file.
        mock_parse_args.return_value = argparse.Namespace(
            repo="owner/repo",
            file="non_existent_file.txt",
            output=None
        )
        mock_open_func.side_effect = FileNotFoundError

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error: Input file not found at 'non_existent_file.txt'", mock_stderr.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_output_file_write_error(self, mock_parse_args, mock_open_func, mock_stderr, mock_stdout):
        # Mock rationale: Simulate an IOError when trying to write to the output file.
        mock_parse_args.return_value = argparse.Namespace(
            repo="owner/repo",
            file=None,
            output="unwritable_file.txt"
        )
        mock_open_func.return_value.__enter__.return_value.write.side_effect = IOError("Disk full")

        with patch('sys.stdin', new_callable=StringIO) as mock_stdin:
            mock_stdin.write("Content to write.")
            mock_stdin.seek(0)

            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error writing output file: Disk full", mock_stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
