import os
import ast
import sys

MIN_DOCSTRING_LENGTH = 15  # Minimum characters for a docstring to be considered 'sufficient'
IGNORED_PATHS = ['venv', '.git', 'node_modules', '__pycache__', 'tests', 'docs'] # Directories to ignore

def is_ignored(path, ignored_paths):
    """Checks if a given path should be ignored based on the IGNORED_PATHS list."""
    # Check if any part of the path contains an ignored directory name
    path_parts = path.split(os.sep)
    for ignored_dir in ignored_paths:
        if ignored_dir in path_parts:
            return True
    return False

def check_docstring(node):
    """Checks if an AST node (FunctionDef or ClassDef) has a sufficient docstring."""
    docstring = ast.get_docstring(node)
    if not docstring or len(docstring.strip()) < MIN_DOCSTRING_LENGTH:
        # Check for common generic docstrings like '""""""' or 'pass'
        if docstring and docstring.strip() in ['""""""', 'pass']:
            return False, "Docstring too short or generic."
        return False, "Missing docstring."
    return True, None

def analyze_file(filepath):
    """Analyzes a single Python file for docstring deficiencies."""
    deficiencies = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                has_docstring, reason = check_docstring(node)
                if not has_docstring:
                    deficiencies.append({
                        'type': 'class' if isinstance(node, ast.ClassDef) else 'function',
                        'name': node.name,
                        'line': node.lineno,
                        'reason': reason
                    })
    except SyntaxError as e:
        deficiencies.append({
            'type': 'file',
            'name': filepath,
            'line': e.lineno,
            'reason': f"Syntax error: {e.msg}"
        })
    except Exception as e:
        deficiencies.append({
            'type': 'file',
            'name': filepath,
            'line': 0,
            'reason': f"Error processing file: {e}"
        })
    return deficiencies

def main(root_dir):
    """Main function to scan the repository for docstring deficiencies."""
    print(f"Scanning directory: {root_dir}\n")
    all_deficiencies = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter dirnames in-place to skip ignored directories for efficiency
        dirnames[:] = [d for d in dirnames if not is_ignored(os.path.join(dirpath, d), IGNORED_PATHS)]

        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                if not is_ignored(filepath, IGNORED_PATHS):
                    file_deficiencies = analyze_file(filepath)
                    if file_deficiencies:
                        all_deficiencies[filepath] = file_deficiencies

    if not all_deficiencies:
        print("No docstring deficiencies found. Your codebase is a beacon of clarity!")
    else:
        print("--- Docstring Deficiencies Found ---")
        for filepath, deficiencies in all_deficiencies.items():
            print(f"\nFile: {filepath}")
            for d in deficiencies:
                print(f"  - {d['type'].capitalize()} '{d['name']}' (line {d['line']}): {d['reason']}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python src/sentinel.py <path_to_repository>")
        sys.exit(1)
    repo_path = sys.argv[1]
    if not os.path.isdir(repo_path):
        print(f"Error: '{repo_path}' is not a valid directory.")
        sys.exit(1)
    main(repo_path)
