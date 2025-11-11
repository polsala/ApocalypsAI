import unittest
from unittest.mock import patch, mock_open
import os
import sys

# Add the src directory to the path to allow importing sentinel
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import sentinel
sys.path.pop(0)

# Access functions/variables via the imported module
analyze_file = sentinel.analyze_file
main = sentinel.main
MIN_DOCSTRING_LENGTH = sentinel.MIN_DOCSTRING_LENGTH
IGNORED_PATHS = sentinel.IGNORED_PATHS

class TestDocstringSentinel(unittest.TestCase):

    def test_analyze_file_perfect_docstrings(self):
        code = """
class MyClass:
    """A class with a good docstring.
    It spans multiple lines for clarity."""
    def __init__(self):
        """Initializes the class instance."""
        pass

    def my_method(self, arg):
        """Performs a useful operation with arg.
        This is a multi-line docstring example."""
        return arg * 2

def my_function(param):
    """A function that does something useful with param.
    Ensures the parameter is processed correctly."""
    return param + 1
"""
        # Mock rationale: Simulate reading a Python file with well-documented code.
        with patch('builtins.open', mock_open(read_data=code)) as mock_file:
            deficiencies = analyze_file('dummy_path/perfect.py')
            self.assertEqual(len(deficiencies), 0)

    def test_analyze_file_missing_function_docstring(self):
        code = """
class MyClass:
    """A class docstring."""
    def method_without_docstring(self):
        pass

def function_without_docstring():
    pass
"""
        # Mock rationale: Simulate reading a Python file where functions lack docstrings.
        with patch('builtins.open', mock_open(read_data=code)) as mock_file:
            deficiencies = analyze_file('dummy_path/missing_func.py')
            self.assertEqual(len(deficiencies), 2)
            self.assertIn({'type': 'function', 'name': 'method_without_docstring', 'line': 4, 'reason': 'Missing docstring.'}, deficiencies)
            self.assertIn({'type': 'function', 'name': 'function_without_docstring', 'line': 7, 'reason': 'Missing docstring.'}, deficiencies)

    def test_analyze_file_missing_class_docstring(self):
        code = """
class ClassWithoutDocstring:
    def __init__(self):
        """Constructor for the class."""
        pass

def some_func():
    """A function that performs a task."""
    pass
"""
        # Mock rationale: Simulate reading a Python file where a class lacks a docstring.
        with patch('builtins.open', mock_open(read_data=code)) as mock_file:
            deficiencies = analyze_file('dummy_path/missing_class.py')
            self.assertEqual(len(deficiencies), 1)
            self.assertIn({'type': 'class', 'name': 'ClassWithoutDocstring', 'line': 2, 'reason': 'Missing docstring.'}, deficiencies)

    def test_analyze_file_short_generic_docstring(self):
        code = f"""
class ShortDocClass:
    """Short."""
    def __init__(self):
        """Init."""
        pass

def empty_doc_func():
    """""" # Empty docstring
    pass

def generic_doc_func():
    """A function."""
    pass
"""
        # Mock rationale: Simulate reading a Python file with docstrings that are too short or generic.
        with patch('builtins.open', mock_open(read_data=code)) as mock_file:
            deficiencies = analyze_file('dummy_path/short_generic.py')
            expected_deficiencies = [
                {'type': 'class', 'name': 'ShortDocClass', 'line': 2, 'reason': 'Docstring too short or generic.'},
                {'type': 'function', 'name': '__init__', 'line': 4, 'reason': 'Docstring too short or generic.'},
                {'type': 'function', 'name': 'empty_doc_func', 'line': 9, 'reason': 'Docstring too short or generic.'}
            ]
            # 'generic_doc_func' should be flagged if its docstring is shorter than MIN_DOCSTRING_LENGTH
            if len("A function.") < MIN_DOCSTRING_LENGTH:
                 expected_deficiencies.append({'type': 'function', 'name': 'generic_doc_func', 'line': 12, 'reason': 'Docstring too short or generic.'})

            self.assertEqual(len(deficiencies), len(expected_deficiencies))
            for expected_def in expected_deficiencies:
                self.assertIn(expected_def, deficiencies)

    def test_analyze_file_syntax_error(self):
        code = """
def func_with_error(
    pass
"""
        # Mock rationale: Simulate reading a Python file with a syntax error.
        with patch('builtins.open', mock_open(read_data=code)) as mock_file:
            deficiencies = analyze_file('dummy_path/syntax_error.py')
            self.assertEqual(len(deficiencies), 1)
            self.assertEqual(deficiencies[0]['type'], 'file')
            self.assertIn('Syntax error', deficiencies[0]['reason'])

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_integration(self, mock_stdout, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a file system structure and content for an end-to-end test of main.
        # This tests os.walk, file reading, and output.

        # Setup mock os.walk to simulate a directory structure
        mock_os_walk.return_value = [
            ('/repo', ['src', 'tests', 'venv'], ['main.py']),
            ('/repo/src', [], ['module_a.py', 'module_b.py']),
            ('/repo/tests', [], ['test_module_a.py']),
            ('/repo/venv', ['lib'], []) # Should be ignored
        ]

        # Define content for mock files
        file_contents = {
            '/repo/main.py': """
def entry_point():
    """""" # Short docstring
    pass
""",
            '/repo/src/module_a.py': """
class GoodClass:
    """This is a good class docstring, providing ample detail."""
    def good_method():
        """This is a good method docstring, explaining its functionality."""
        pass

class BadClass:
    def bad_method():
        pass
""",
            '/repo/src/module_b.py': """
def another_func():
    pass
""",
            '/repo/tests/test_module_a.py': """
import unittest
class TestModuleA(unittest.TestCase):
    def test_something(self):
        pass
"""
        }

        # Configure mock_file_open to return specific content based on path
        def mock_open_side_effect(filepath, *args, **kwargs):
            if filepath in file_contents:
                return mock_open(read_data=file_contents[filepath]).return_value
            raise FileNotFoundError(f"No mock content for {filepath}")

        mock_file_open.side_effect = mock_open_side_effect

        # Run main function
        main('/repo')

        output = mock_stdout.getvalue()

        # Assertions for expected output
        self.assertIn("Scanning directory: /repo", output)
        self.assertIn("--- Docstring Deficiencies Found ---", output)

        # Check main.py deficiency
        self.assertIn("File: /repo/main.py", output)
        self.assertIn("Function 'entry_point' (line 2): Docstring too short or generic.", output)

        # Check module_a.py deficiencies
        self.assertIn("File: /repo/src/module_a.py", output)
        self.assertIn("Class 'BadClass' (line 8): Missing docstring.", output)
        self.assertIn("Function 'bad_method' (line 9): Missing docstring.", output)

        # Check module_b.py deficiency
        self.assertIn("File: /repo/src/module_b.py", output)
        self.assertIn("Function 'another_func' (line 2): Missing docstring.", output)

        # Ensure tests directory was ignored (no deficiencies reported from test_module_a.py)
        self.assertNotIn("File: /repo/tests/test_module_a.py", output)
        self.assertNotIn("Class 'TestModuleA'", output)
        self.assertNotIn("Function 'test_something'", output)

        # Ensure venv directory was ignored
        self.assertNotIn("/repo/venv", output)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_no_deficiencies(self, mock_stdout, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate a repository with no docstring issues to verify the success message.
        mock_os_walk.return_value = [
            ('/repo', ['src'], ['perfect.py']),
            ('/repo/src', [], ['another_perfect.py'])
        ]
        file_contents = {
            '/repo/perfect.py': """
def func_a():
    """This is a good docstring for func_a, providing sufficient detail."""
    pass
""",
            '/repo/src/another_perfect.py': """
class PerfectClass:
    """This is a good docstring for PerfectClass, explaining its purpose."""
    def method_b(self):
        """This is a good docstring for method_b, detailing its operation."""
        pass
"""
        }
        def mock_open_side_effect(filepath, *args, **kwargs):
            if filepath in file_contents:
                return mock_open(read_data=file_contents[filepath]).return_value
            raise FileNotFoundError(f"No mock content for {filepath}")
        mock_file_open.side_effect = mock_open_side_effect

        main('/repo')
        output = mock_stdout.getvalue()
        self.assertIn("No docstring deficiencies found. Your codebase is a beacon of clarity!", output)
        self.assertNotIn("--- Docstring Deficiencies Found ---", output)

    def test_is_ignored_functionality(self):
        # Mock rationale: Test the utility's path ignoring logic without actual file system access.
        self.assertTrue(sentinel.is_ignored('/path/to/venv/script.py', IGNORED_PATHS))
        self.assertTrue(sentinel.is_ignored('/path/to/.git/hooks/pre-commit', IGNORED_PATHS))
        self.assertTrue(sentinel.is_ignored('/path/to/node_modules/package/index.js', IGNORED_PATHS))
        self.assertTrue(sentinel.is_ignored('/path/to/tests/test_file.py', IGNORED_PATHS))
        self.assertFalse(sentinel.is_ignored('/path/to/my_project/script.py', IGNORED_PATHS))
        self.assertFalse(sentinel.is_ignored('/path/to/my_project/src/file.py', IGNORED_PATHS))
        self.assertTrue(sentinel.is_ignored('/repo/venv', IGNORED_PATHS)) # Test directory itself
        self.assertTrue(sentinel.is_ignored('/repo/tests', IGNORED_PATHS)) # Test directory itself
        self.assertFalse(sentinel.is_ignored('/repo/src', IGNORED_PATHS))


if __name__ == '__main__':
    unittest.main()
