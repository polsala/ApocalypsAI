import unittest
from unittest.mock import patch, mock_open
import os
import sys
import ast

# Add the src directory to the path to allow importing gardener
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from gardener import find_unused_dependencies, _normalize_package_name, _parse_requirements_txt, _parse_pyproject_toml, _find_python_imports, ImportCollector


class TestGardener(unittest.TestCase):

    def test_normalize_package_name(self):
        self.assertEqual(_normalize_package_name('requests'), 'requests')
        self.assertEqual(_normalize_package_name('my-package'), 'my_package')
        self.assertEqual(_normalize_package_name('My_Package'), 'my_package')
        self.assertEqual(_normalize_package_name('requests==2.28.1'), 'requests')
        self.assertEqual(_normalize_package_name('Django>=3.0'), 'django')
        self.assertEqual(_normalize_package_name('numpy~=1.20'), 'numpy')
        self.assertEqual(_normalize_package_name('package<1.0'), 'package')
        self.assertEqual(_normalize_package_name('package>1.0'), 'package')
        self.assertEqual(_normalize_package_name('package[extra]'), 'package')
        self.assertEqual(_normalize_package_name('package[extra]==1.0'), 'package')

    @patch('builtins.open', new_callable=mock_open)
    def test_parse_requirements_txt(self, mock_file_open):
        # Mock rationale: Simulates reading a requirements.txt file without actual file I/O.
        mock_file_open.return_value.read.return_value = (
            "requests==2.28.1\n"
            "# This is a comment\n"
            "my-package>=1.0.0\n"
            "another_lib\n"
            "  -e git+https://github.com/user/repo.git#egg=editable-package\n"
            "package-with-extras[test]>=1.0\n"
        )
        expected_deps = {'requests', 'my_package', 'another_lib', 'package_with_extras'}
        self.assertEqual(_parse_requirements_txt('reqs.txt'), expected_deps)

        mock_file_open.return_value.read.return_value = ""
        self.assertEqual(_parse_requirements_txt('empty.txt'), set())

        # Test IOError
        mock_file_open.side_effect = IOError("File not found")
        with patch('builtins.print') as mock_print:
            self.assertEqual(_parse_requirements_txt('nonexistent.txt'), set())
            mock_print.assert_called_with(unittest.mock.ANY)

    @patch('builtins.open', new_callable=mock_open)
    @patch('gardener.tomli') # Mock rationale: Prevents actual import of tomli and allows control over its load method.
    def test_parse_pyproject_toml(self, mock_tomli, mock_file_open):
        mock_tomli.load.return_value = {
            'project': {
                'name': 'my-project',
                'dependencies': [
                    'requests>=2.0',
                    'pydantic',
                    'toml-package~=0.1.0',
                    'another-package[dev]'
                ]
            }
        }
        expected_deps = {'requests', 'pydantic', 'toml_package', 'another_package'}
        self.assertEqual(_parse_pyproject_toml('pyproject.toml'), expected_deps)

        # Test with no project dependencies
        mock_tomli.load.return_value = {'project': {'name': 'my-project'}}
        self.assertEqual(_parse_pyproject_toml('pyproject.toml'), set())

        # Test with no tomli available
        with patch('gardener.tomli', None):
            with patch('builtins.print') as mock_print:
                self.assertEqual(_parse_pyproject_toml('pyproject.toml'), set())
                mock_print.assert_called_with("Warning: 'tomli' not found. Cannot parse pyproject.toml for dependencies.")

        # Test TomlDecodeError
        mock_tomli.load.side_effect = tomli.TomlDecodeError("Invalid TOML")
        with patch('builtins.print') as mock_print:
            self.assertEqual(_parse_pyproject_toml('bad_pyproject.toml'), set())
            mock_print.assert_called_with(unittest.mock.ANY)

    def test_import_collector(self):
        tree = ast.parse(
            "import os\n"
            "import sys, json\n"
            "from collections import defaultdict\n"
            "from my_module.sub_module import func\n"
            "import requests.exceptions as req_exc\n"
            "from . import local_module\n"
            "from .. import parent_module\n"
            "from some_package.sub_package import ClassName\n"
        )
        collector = ImportCollector()
        collector.visit(tree)
        expected_imports = {'os', 'sys', 'json', 'collections', 'my_module', 'requests', 'local_module', 'parent_module', 'some_package'}
        self.assertEqual(collector.imports, expected_imports)

    @patch('builtins.open', new_callable=mock_open)
    @patch('gardener.ast.parse') # Mock rationale: Prevents actual parsing of Python code, allowing control over the AST result.
    def test_find_python_imports(self, mock_ast_parse, mock_file_open):
        mock_file_open.return_value.read.return_value = "import foo\nfrom bar import baz"
        mock_ast_parse.return_value = ast.parse("import foo\nfrom bar import baz") # Provide a simple AST
        self.assertEqual(_find_python_imports('my_script.py'), {'foo', 'bar'})

        # Test syntax error handling
        mock_ast_parse.side_effect = SyntaxError("invalid syntax")
        with patch('builtins.print') as mock_print:
            self.assertEqual(_find_python_imports('bad_script.py'), set())
            mock_print.assert_called_with(unittest.mock.ANY) # Check if print was called, content less important for this test

        # Test generic exception handling
        mock_ast_parse.side_effect = Exception("unexpected error")
        with patch('builtins.print') as mock_print:
            self.assertEqual(_find_python_imports('error_script.py'), set())
            mock_print.assert_called_with(unittest.mock.ANY)

    @patch('os.walk') # Mock rationale: Controls the file system traversal without actual disk access.
    @patch('builtins.open', new_callable=mock_open) # Mock rationale: Simulates reading file contents.
    @patch('gardener.tomli') # Mock rationale: Controls tomli.load behavior.
    @patch('gardener.ast.parse') # Mock rationale: Controls AST parsing for Python files.
    @patch('builtins.print') # Mock rationale: Suppress print statements during tests and check output if needed.
    def test_find_unused_dependencies_all_used(self, mock_print, mock_ast_parse, mock_tomli, mock_file_open, mock_os_walk):
        # Setup mock file system
        mock_os_walk.return_value = [
            ('.', ['src'], ['requirements.txt', 'pyproject.toml']),
            ('./src', [], ['main.py', 'utils.py'])
        ]

        # Mock file contents
        def mock_open_side_effect(filepath, mode='r', encoding='utf-8'):
            if 'requirements.txt' in filepath:
                return mock_open(read_data="requests\nflask").return_value
            elif 'pyproject.toml' in filepath:
                mock_tomli.load.return_value = {'project': {'dependencies': ['pydantic']}}
                return mock_open(read_data="[project]\ndependencies = [\"pydantic\"]").return_value
            elif 'main.py' in filepath:
                return mock_open(read_data="import requests\nfrom flask import Flask").return_value
            elif 'utils.py' in filepath:
                return mock_open(read_data="from pydantic import BaseModel").return_value
            return mock_open().return_value

        mock_file_open.side_effect = mock_open_side_effect

        # Mock AST parsing for Python files
        def mock_ast_parse_side_effect(source, filename):
            if 'main.py' in filename:
                return ast.parse("import requests\nfrom flask import Flask")
            elif 'utils.py' in filename:
                return ast.parse("from pydantic import BaseModel")
            return ast.parse("")

        mock_ast_parse.side_effect = mock_ast_parse_side_effect

        unused = find_unused_dependencies('.')
        self.assertEqual(unused, [])
        mock_print.assert_any_call("\nProject is clean of unused dependencies.")

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('gardener.tomli')
    @patch('gardener.ast.parse')
    @patch('builtins.print')
    def test_find_unused_dependencies_some_unused(self, mock_print, mock_ast_parse, mock_tomli, mock_file_open, mock_os_walk):
        mock_os_walk.return_value = [
            ('.', ['src'], ['requirements.txt']),
            ('./src', [], ['app.py'])
        ]

        def mock_open_side_effect(filepath, mode='r', encoding='utf-8'):
            if 'requirements.txt' in filepath:
                return mock_open(read_data="requests\nunused-lib\nflask").return_value
            elif 'app.py' in filepath:
                return mock_open(read_data="import requests\nfrom flask import Flask").return_value
            return mock_open().return_value

        mock_file_open.side_effect = mock_open_side_effect

        def mock_ast_parse_side_effect(source, filename):
            if 'app.py' in filename:
                return ast.parse("import requests\nfrom flask import Flask")
            return ast.parse("")

        mock_ast_parse.side_effect = mock_ast_parse_side_effect

        unused = find_unused_dependencies('.')
        self.assertEqual(unused, ['unused_lib']) # Normalized name
        mock_print.assert_any_call("\n--- Unused Dependencies Found ---")
        mock_print.assert_any_call("- unused_lib")

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('gardener.tomli')
    @patch('gardener.ast.parse')
    @patch('builtins.print')
    def test_find_unused_dependencies_no_deps_declared(self, mock_print, mock_ast_parse, mock_tomli, mock_file_open, mock_os_walk):
        mock_os_walk.return_value = [
            ('.', ['src'], []),
            ('./src', [], ['app.py'])
        ]

        def mock_open_side_effect(filepath, mode='r', encoding='utf-8'):
            if 'app.py' in filepath:
                return mock_open(read_data="import requests").return_value
            return mock_open().return_value

        mock_file_open.side_effect = mock_open_side_effect

        def mock_ast_parse_side_effect(source, filename):
            if 'app.py' in filename:
                return ast.parse("import requests")
            return ast.parse("")

        mock_ast_parse.side_effect = mock_ast_parse_side_effect

        unused = find_unused_dependencies('.')
        self.assertEqual(unused, [])
        mock_print.assert_any_call("Found 0 declared dependencies.")
        mock_print.assert_any_call("\nProject is clean of unused dependencies.")

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('gardener.tomli')
    @patch('gardener.ast.parse')
    @patch('builtins.print')
    def test_find_unused_dependencies_no_python_files(self, mock_print, mock_ast_parse, mock_tomli, mock_file_open, mock_os_walk):
        mock_os_walk.return_value = [
            ('.', [], ['requirements.txt'])
        ]

        def mock_open_side_effect(filepath, mode='r', encoding='utf-8'):
            if 'requirements.txt' in filepath:
                return mock_open(read_data="requests").return_value
            return mock_open().return_value

        mock_file_open.side_effect = mock_open_side_effect

        unused = find_unused_dependencies('.')
        self.assertEqual(unused, ['requests'])
        mock_print.assert_any_call("Found 1 declared dependencies.")
        mock_print.assert_any_call("Found 0 active imports.")
        mock_print.assert_any_call("- requests")


if __name__ == '__main__':
    unittest.main()
