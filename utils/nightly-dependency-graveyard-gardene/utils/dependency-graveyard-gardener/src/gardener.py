import os
import re
import ast
from typing import Set, List, Dict

try:
    import tomli
except ImportError:
    # Fallback for older Python versions or environments without tomli
    # AGENTS.md allows tomli, but we provide a graceful degradation.
    tomli = None


def _normalize_package_name(name: str) -> str:
    """Normalizes a package name for comparison (e.g., 'package-name' -> 'package_name')."""
    # Remove version specifiers and extras, then normalize to lowercase and replace hyphens with underscores
    normalized = re.split(r'[<=>~!\[]', name)[0].strip()
    return normalized.lower().replace('-', '_')


def _parse_requirements_txt(filepath: str) -> Set[str]:
    """Parses a requirements.txt file and returns a set of normalized package names."""
    declared_deps = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Basic parsing, ignores versions for now
                    dep_name = _normalize_package_name(line)
                    if dep_name:
                        declared_deps.add(dep_name)
    except IOError as e:
        print(f"Warning: Could not read requirements.txt at {filepath}: {e}")
    return declared_deps


def _parse_pyproject_toml(filepath: str) -> Set[str]:
    """Parses pyproject.toml for [project].dependencies and returns a set of normalized package names."""
    if not tomli:
        print("Warning: 'tomli' not found. Cannot parse pyproject.toml for dependencies.")
        return set()

    declared_deps = set()
    try:
        with open(filepath, 'rb') as f:
            data = tomli.load(f)
            project_deps = data.get('project', {}).get('dependencies', [])
            for dep in project_deps:
                dep_name = _normalize_package_name(dep)
                if dep_name:
                    declared_deps.add(dep_name)
    except (IOError, tomli.TomlDecodeError) as e:
        print(f"Warning: Could not parse pyproject.toml at {filepath}: {e}")
    return declared_deps


class ImportCollector(ast.NodeVisitor):
    """Collects all imported module names from a Python AST."""
    def __init__(self):
        self.imports = set()

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.add(_normalize_package_name(alias.name.split('.')[0]))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            # Handle relative imports by taking the first part of the module name
            # e.g., 'my_package.sub_module' -> 'my_package'
            # e.g., '.local_module' -> 'local_module'
            # e.g., '..parent_module' -> 'parent_module'
            module_name = node.module.lstrip('.')
            if module_name:
                self.imports.add(_normalize_package_name(module_name.split('.')[0]))
        self.generic_visit(node)


def _find_python_imports(filepath: str) -> Set[str]:
    """Parses a Python file and returns a set of normalized imported module names."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
            collector = ImportCollector()
            collector.visit(tree)
            return collector.imports
    except SyntaxError as e:
        print(f"Warning: Could not parse {filepath} due to syntax error: {e}")
        return set()
    except Exception as e:
        print(f"Warning: An unexpected error occurred while parsing {filepath}: {e}")
        return set()


def find_unused_dependencies(project_root: str = '.') -> List[str]:
    """
    Scans the project root for declared dependencies and actual imports,
    returning a list of unused dependency names.
    """
    all_declared_deps: Set[str] = set()
    all_active_imports: Set[str] = set()

    print(f"Scanning project '{project_root}' for unused dependencies...")

    for root, _, files in os.walk(project_root):
        for file in files:
            filepath = os.path.join(root, file)

            # Collect declared dependencies
            if file == 'requirements.txt':
                all_declared_deps.update(_parse_requirements_txt(filepath))
            elif file == 'pyproject.toml':
                all_declared_deps.update(_parse_pyproject_toml(filepath))

            # Collect active imports from Python files
            if file.endswith('.py'):
                all_active_imports.update(_find_python_imports(filepath))

    print(f"Found {len(all_declared_deps)} declared dependencies.")
    print(f"Found {len(all_active_imports)} active imports.")

    unused_deps = sorted(list(all_declared_deps - all_active_imports))

    if not unused_deps:
        print("\nProject is clean of unused dependencies.")
    else:
        print("\n--- Unused Dependencies Found ---")
        for dep in unused_deps:
            print(f"- {dep}")
        print("---------------------------------")

    return unused_deps


if __name__ == '__main__':
    # Example usage when run as a script
    find_unused_dependencies()
