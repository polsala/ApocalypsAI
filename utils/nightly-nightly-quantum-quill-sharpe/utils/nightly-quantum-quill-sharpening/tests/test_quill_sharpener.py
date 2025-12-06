import unittest
import os
from unittest.mock import patch, mock_open
from io import StringIO
import sys
import argparse

# Mock rationale: We need to simulate file system interactions (os.walk, open) and
# command-line arguments (argparse) without actually touching the disk or parsing real files.
# This ensures tests are deterministic, fast, and isolated from the environment.

class TestQuillSharpener(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = StringIO()
        self.stdout_patcher = patch('sys.stdout', self.held_stdout)
        self.stdout_patcher.start()

        # Mock rationale: Adjust sys.path to allow relative import of the utility module
        # when running tests from within the 'tests' directory of the utility.
        # This ensures the utility is self-contained and runnable in its own venv.
        current_dir = os.path.dirname(__file__)
        src_dir = os.path.join(current_dir, '..', 'src')
        sys.path.insert(0, src_dir)
        
        global quill_sharpener
        import quill_sharpener # Now it can be imported directly
        
    def tearDown(self):
        self.stdout_patcher.stop()
        # Clean up sys.path
        current_dir = os.path.dirname(__file__)
        src_dir = os.path.join(current_dir, '..', 'src')
        if src_dir in sys.path:
            sys.path.remove(src_dir)
        # Remove from loaded modules to prevent interference between tests if module state changes
        if 'quill_sharpener' in sys.modules:
            del sys.modules['quill_sharpener'] 
        del quill_sharpener # Clean up imported module

    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_python_file_with_docstrings_and_comments(self, mock_file_open):
        mock_file_open.return_value.read.return_value = """
# This is a module-level comment

class MyClass:
    """A class with a docstring."""
    def __init__(self):
        # Constructor comment
        pass

    def my_method(self, arg):
        """A method with a docstring."""
        return arg

def my_function(param):
    """A function with a docstring."""
    # Function logic comment
    return param * 2
"""
        
        result = quill_sharpener.analyze_python_file("dummy_path/test_file.py")
        self.assertEqual(result['filepath'], "dummy_path/test_file.py")
        self.assertEqual(result['missing_docstrings'], [])
        # Expected lines: 1 (module comment) + 1 (constructor comment) + 1 (function logic comment) = 3 comment lines
        # Total lines: 1 (module comment) + 1 (blank) + 1 (class def) + 1 (class doc) + 1 (init def) + 1 (init comment) + 1 (pass) + 1 (blank) + 1 (method def) + 1 (method doc) + 1 (return) + 1 (blank) + 1 (func def) + 1 (func doc) + 1 (func comment) + 1 (return) = 16 lines
        # Density: (3/16) * 100 = 18.75%
        self.assertAlmostEqual(result['comment_density'], (3/16)*100, places=2)
        self.assertEqual(result['total_lines'], 16)
        self.assertEqual(result['comment_lines'], 3)

    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_python_file_missing_docstrings_and_low_comments(self, mock_file_open):
        mock_file_open.return_value.read.return_value = """
class NoDocClass:
    def __init__(self):
        pass

def no_doc_func():
    pass

# Only one comment line
"""
        result = quill_sharpener.analyze_python_file("dummy_path/another_file.py")
        self.assertEqual(result['filepath'], "dummy_path/another_file.py")
        self.assertIn('- Class: NoDocClass', result['missing_docstrings'])
        self.assertIn('- Function: no_doc_func', result['missing_docstrings'])
        self.assertEqual(len(result['missing_docstrings']), 2)
        # Expected lines: 1 comment line
        # Total lines: 1 (class def) + 1 (init def) + 1 (pass) + 1 (blank) + 1 (func def) + 1 (pass) + 1 (blank) + 1 (comment) = 8 lines
        # Density: (1/8) * 100 = 12.5%
        self.assertAlmostEqual(result['comment_density'], (1/8)*100, places=2)
        self.assertEqual(result['total_lines'], 8)
        self.assertEqual(result['comment_lines'], 1)

    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_empty_file(self, mock_file_open):
        mock_file_open.return_value.read.return_value = """
"""
        result = quill_sharpener.analyze_python_file("dummy_path/empty.py")
        self.assertEqual(result['filepath'], "dummy_path/empty.py")
        self.assertEqual(result['missing_docstrings'], [])
        self.assertEqual(result['comment_density'], 0.0)
        self.assertEqual(result['total_lines'], 0) # Corrected: empty string has 0 lines after splitlines()
        self.assertEqual(result['comment_lines'], 0)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_report_generation(self, mock_parse_args, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate command-line arguments, file system traversal, and file content.
        # This allows testing the end-to-end flow of the main function without actual file I/O.

        mock_parse_args.return_value = argparse.Namespace(
            path="/mock/project",
            min_comment_density=15.0
        )

        # Simulate os.walk returning two Python files
        mock_os_walk.return_value = [
            ('/mock/project', [], ['file_a.py', 'file_b.py'])
        ]

        # Configure mock_file_open for each file
        file_contents = {
            os.path.join('/mock/project', 'file_a.py'): """
# Comment 1
class MyClass:
    def method_a():
        pass
""",
            os.path.join('/mock/project', 'file_b.py'): """
"""""A module docstring""""
def func_b():
    """Docstring for func_b"""
    # Inline comment
    pass
"""
        }

        def mock_open_side_effect(filepath, *args, **kwargs):
            if filepath in file_contents:
                return mock_open(read_data=file_contents[filepath]).return_value
            raise FileNotFoundError(f"No mock content for {filepath}")

        mock_file_open.side_effect = mock_open_side_effect

        # Mock os.path.isdir to return True for the target_dir
        with patch('os.path.isdir', return_value=True):
            quill_sharpener.main()

        output = self.held_stdout.getvalue()
        self.assertIn("Quantum Quill Sharpening Report", output)
        self.assertIn(f"Scanning directory: {mock_parse_args.return_value.path}", output)

        # Verify file_a.py analysis
        self.assertIn("File: /mock/project/file_a.py", output)
        # file_a: 1 comment, 4 total lines -> 25% density
        self.assertIn("Comment Density: 25.00%", output)
        self.assertNotIn("(Below 15.00% threshold)", output) # 25% > 15%
        self.assertIn("Missing Docstrings:", output)
        self.assertIn("    - Class: MyClass", output)
        self.assertIn("    - Function: method_a", output)

        # Verify file_b.py analysis
        self.assertIn("File: /mock/project/file_b.py", output)
        # file_b: 1 comment, 5 total lines -> 20% density
        self.assertIn("Comment Density: 20.00%", output)
        self.assertNotIn("(Below 15.00% threshold)", output) # 20% > 15%
        self.assertIn("Missing Docstrings: None", output)

        # Verify summary
        self.assertIn("Total files scanned: 2", output)
        self.assertIn("Files with low comment density: 0", output)
        self.assertIn("Total missing docstrings: 2", output)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_no_python_files(self, mock_parse_args, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a directory with no Python files to test the 'no files found' scenario.
        mock_parse_args.return_value = argparse.Namespace(
            path="/mock/empty_project",
            min_comment_density=10.0
        )
        mock_os_walk.return_value = [
            ('/mock/empty_project', [], ['text.txt', 'image.png'])
        ]
        with patch('os.path.isdir', return_value=True):
            quill_sharpener.main()
        output = self.held_stdout.getvalue()
        self.assertIn("No Python files found in '/mock/empty_project'.", output)

    @patch('os.path.isdir', return_value=False)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_invalid_path(self, mock_parse_args, mock_isdir):
        # Mock rationale: Simulate an invalid path argument to test error handling.
        mock_parse_args.return_value = argparse.Namespace(
            path="/non/existent/path",
            min_comment_density=10.0
        )
        with self.assertRaises(SystemExit) as cm:
            quill_sharpener.main()
        self.assertEqual(cm.exception.code, 1)
        output = self.held_stdout.getvalue()
        self.assertIn("Error: Directory '/non/existent/path' not found.", output)

if __name__ == '__main__':
    unittest.main()
