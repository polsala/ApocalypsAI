import unittest
from unittest.mock import patch, mock_open
import sys
import os
import subprocess

# Add the src directory to the path to allow importing diff_summarizer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import diff_summarizer

class TestDiffSummarizer(unittest.TestCase):

    def test_parse_diff_empty(self):
        # Test with an empty diff
        diff_content = ""
        summary = diff_summarizer.parse_diff(diff_content)
        self.assertEqual(summary['lines_added'], 0)
        self.assertEqual(summary['lines_removed'], 0)
        self.assertEqual(summary['files_changed'], [])

    def test_parse_diff_single_file_add(self):
        # Test adding a new file
        diff_content = """
diff --git a/new_file.txt b/new_file.txt
new file mode 100644
index 0000000..e69de29
--- /dev/null
+++ b/new_file.txt
@@ -0,0 +1,3 @@
+Line 1
+Line 2
+Line 3
"""
        summary = diff_summarizer.parse_diff(diff_content)
        self.assertEqual(summary['lines_added'], 3)
        self.assertEqual(summary['lines_removed'], 0)
        self.assertEqual(summary['files_changed'], ['new_file.txt'])

    def test_parse_diff_single_file_modify(self):
        # Test modifying an existing file
        diff_content = """
diff --git a/existing.py b/existing.py
index a1b2c3d..e4f5g6h 100644
--- a/existing.py
+++ b/existing.py
@@ -1,4 +1,4 @@
 def hello():
-    print("Hello, World!")
+    print("Hello, ApocalypsAI!")
     pass
-print("End")
+print("The End")
"""
        summary = diff_summarizer.parse_diff(diff_content)
        self.assertEqual(summary['lines_added'], 2)
        self.assertEqual(summary['lines_removed'], 2)
        self.assertEqual(summary['files_changed'], ['existing.py'])

    def test_parse_diff_single_file_delete(self):
        # Test deleting a file
        diff_content = """
diff --git a/old_file.md b/old_file.md
deleted file mode 100644
index e69de29..0000000
--- a/old_file.md
+++ /dev/null
@@ -1,2 +0,0 @@
-This is an old file.
-It will be deleted.
"""
        summary = diff_summarizer.parse_diff(diff_content)
        self.assertEqual(summary['lines_added'], 0)
        self.assertEqual(summary['lines_removed'], 2)
        self.assertEqual(summary['files_changed'], ['old_file.md'])

    def test_parse_diff_multiple_files(self):
        # Test diff with multiple files
        diff_content = """
diff --git a/file1.txt b/file1.txt
index 1234567..abcdef0 100644
--- a/file1.txt
+++ b/file1.txt
@@ -1,2 +1,3 @@
 Line A
+Line B_new
 Line C
diff --git a/dir/file2.py b/dir/file2.py
index fedcba9..0987654 100644
--- a/dir/file2.py
+++ b/dir/file2.py
@@ -1,3 +1,2 @@
-import os
 def func():
     pass
"""
        summary = diff_summarizer.parse_diff(diff_content)
        self.assertEqual(summary['lines_added'], 1)
        self.assertEqual(summary['lines_removed'], 1)
        self.assertEqual(summary['files_changed'], ['dir/file2.py', 'file1.txt']) # Sorted list

    @patch('subprocess.run')
    def test_get_git_diff_success(self, mock_run):
        # Mock rationale: Simulate successful git diff command execution.
        mock_run.return_value.stdout = "mock diff output"
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        mock_run.return_value.check_returncode = lambda: None # Mock check_returncode to not raise

        diff = diff_summarizer.get_git_diff('HEAD~1', 'HEAD')
        self.assertEqual(diff, "mock diff output")
        mock_run.assert_called_once_with(
            ['git', 'diff', 'HEAD~1', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    def test_get_git_diff_failure(self, mock_run):
        # Mock rationale: Simulate a failed git diff command execution.
        mock_run.side_effect = subprocess.CalledProcessError(1, ['git', 'diff'], stderr='fatal: bad object')

        with self.assertRaises(SystemExit) as cm:
            diff_summarizer.get_git_diff('bad_ref', 'HEAD')
        self.assertEqual(cm.exception.code, 1)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="file diff content")
    @patch('diff_summarizer.parse_diff', return_value={'lines_added': 1, 'lines_removed': 1, 'files_changed': ['test.txt']})
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_from_file_success(self, mock_stderr, mock_stdout, mock_parse_diff, mock_open_file, mock_exists):
        # Mock rationale: Simulate reading a diff from a file and successful parsing/output.
        test_args = ['diff_summarizer.py', '--file', 'test.diff']
        with patch('sys.argv', test_args):
            diff_summarizer.main()
            self.assertIn("Total Lines Added: 1", mock_stdout.getvalue())
            self.assertIn("Files Changed:\n- test.txt", mock_stdout.getvalue())
            mock_open_file.assert_called_once_with('test.diff', 'r', encoding='utf-8')
            mock_parse_diff.assert_called_once_with("file diff content")

    @patch('subprocess.run')
    @patch('diff_summarizer.parse_diff', return_value={'lines_added': 5, 'lines_removed': 2, 'files_changed': ['script.py']})
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_from_git_refs_success(self, mock_stderr, mock_stdout, mock_parse_diff, mock_run):
        # Mock rationale: Simulate successful git diff execution and parsing/output.
        mock_run.return_value.stdout = "git diff content"
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        mock_run.return_value.check_returncode = lambda: None

        test_args = ['diff_summarizer.py', 'HEAD~1', 'HEAD']
        with patch('sys.argv', test_args):
            diff_summarizer.main()
            self.assertIn("Total Lines Added: 5", mock_stdout.getvalue())
            self.assertIn("Files Changed:\n- script.py", mock_stdout.getvalue())
            mock_run.assert_called_once_with(
                ['git', 'diff', 'HEAD~1', 'HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            mock_parse_diff.assert_called_once_with("git diff content")

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_no_args(self, mock_stderr, mock_stdout):
        # Mock rationale: Test argument parsing failure when no arguments are provided.
        test_args = ['diff_summarizer.py']
        with patch('sys.argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                diff_summarizer.main()
            self.assertEqual(cm.exception.code, 2) # argparse exits with 2 for invalid args
            self.assertIn("error: Either provide two Git references or use the --file option.", mock_stderr.getvalue())

    @patch('os.path.exists', return_value=False)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_file_not_found(self, mock_stderr, mock_stdout, mock_exists):
        # Mock rationale: Test argument parsing failure when the specified diff file does not exist.
        test_args = ['diff_summarizer.py', '--file', 'non_existent.diff']
        with patch('sys.argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                diff_summarizer.main()
            self.assertEqual(cm.exception.code, 2)
            self.assertIn("error: Diff file not found: non_existent.diff", mock_stderr.getvalue())

    @patch('subprocess.run')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_git_diff_no_content(self, mock_stderr, mock_stdout, mock_run):
        # Mock rationale: Simulate git diff returning no content (e.g., no changes between refs).
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        mock_run.return_value.check_returncode = lambda: None

        test_args = ['diff_summarizer.py', 'HEAD', 'HEAD']
        with patch('sys.argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                diff_summarizer.main()
            self.assertEqual(cm.exception.code, 0)
            self.assertIn("No diff content to summarize.", mock_stdout.getvalue())

    @patch('subprocess.run')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_git_command_not_found(self, mock_stderr, mock_stdout, mock_run):
        # Mock rationale: Simulate FileNotFoundError if 'git' command is not found.
        mock_run.side_effect = FileNotFoundError

        test_args = ['diff_summarizer.py', 'HEAD~1', 'HEAD']
        with patch('sys.argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                diff_summarizer.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error: Git command not found.", mock_stderr.getvalue())

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_main_file_read_error(self, mock_stderr, mock_stdout, mock_open_file, mock_exists):
        # Mock rationale: Simulate an IOError when trying to read the diff file.
        mock_open_file.side_effect = IOError("Permission denied")

        test_args = ['diff_summarizer.py', '--file', 'unreadable.diff']
        with patch('sys.argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                diff_summarizer.main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Error reading diff file: Permission denied", mock_stderr.getvalue())
