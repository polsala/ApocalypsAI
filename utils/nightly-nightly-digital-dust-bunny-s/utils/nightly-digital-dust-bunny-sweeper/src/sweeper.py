import os
import argparse
import sys

# Default patterns for common 'dust bunnies' (temporary files, cache directories, build artifacts)
DEFAULT_PATTERNS = [
    '__pycache__',
    '.pytest_cache',
    '.mypy_cache',
    '*.pyc',
    '*.log',
    '*.tmp',
    '*.bak',
    '.DS_Store',
    'Thumbs.db',
    'node_modules',
    'venv',
    '.venv',
    'target', # Rust
    'build',  # Java, Go, JS
    'dist',   # JS
    'out',    # various
    '.idea',  # IntelliJ/PyCharm IDE files
    '.vscode',# VS Code IDE files
    '*.swp',  # Vim swap files
    '*.swo',  # Vim swap files
    '*.orig', # Merge conflict backups
    '*.rej',  # Patch reject files
    'npm-debug.log',
    'yarn-error.log',
    'coverage/', # Test coverage reports
    '.coverage', # Python coverage file
    '*.iml', # IntelliJ module files
    '*.ipr', # IntelliJ project files
    '*.iws', # IntelliJ workspace files
]

def find_dust_bunnies(root_path: str, patterns: list[str]) -> list[str]:
    """
    Scans the given root_path for files and directories matching the provided patterns.
    Returns a list of paths identified as 'dust bunnies'.
    """
    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.", file=sys.stderr)
        return []

    dust_bunnies = set()
    ignored_dirs = set() # To avoid re-scanning directories like node_modules once found

    for root, dirs, files in os.walk(root_path, topdown=True):
        # Filter out ignored_dirs from current dirs list to prevent descending into them
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in ignored_dirs]

        for pattern in patterns:
            is_dir_pattern = pattern.endswith('/') or ('.' not in pattern and '*' not in pattern) # Heuristic for specific directory names
            is_wildcard_pattern = '*' in pattern

            if is_dir_pattern and not is_wildcard_pattern: # Specific directory name (e.g., 'node_modules', '__pycache__')
                for d in list(dirs): # Iterate over a copy to allow modification
                    if d == pattern.strip('/'):
                        full_path = os.path.join(root, d)
                        dust_bunnies.add(full_path)
                        ignored_dirs.add(full_path) # Mark for skipping further traversal
                        dirs.remove(d) # Remove from dirs to prevent os.walk from descending

            elif is_wildcard_pattern: # Wildcard pattern (e.g., '*.log', '*.pyc')
                for f in files:
                    if _match_wildcard(f, pattern):
                        dust_bunnies.add(os.path.join(root, f))

            else: # Specific file name (e.g., 'npm-debug.log')
                for f in files:
                    if f == pattern:
                        dust_bunnies.add(os.path.join(root, f))

    return sorted(list(dust_bunnies))

def _match_wildcard(filename: str, pattern: str) -> bool:
    """
    Simple wildcard matching for patterns like '*.log'.
    Supports only leading wildcard for now.
    """
    if pattern.startswith('*'):
        return filename.endswith(pattern[1:])
    return False

def generate_cleanup_command(path: str) -> str:
    """
    Generates an appropriate cleanup command for a given path.
    """
    if os.path.isdir(path):
        if sys.platform == 'win32':
            return f"rd /s /q \"{path}\"" # Windows remove directory recursively and quietly
        else:
            return f"rm -rf \"{path}\"" # Unix-like remove recursively and forcefully
    else:
        if sys.platform == 'win32':
            return f"del /f /q \"{path}\"" # Windows delete file forcefully and quietly
        else:
            return f"rm -f \"{path}\"" # Unix-like remove file forcefully

def main():
    parser = argparse.ArgumentParser(
        description="Scan for and report 'digital dust bunnies' (temporary files, cache, build artifacts)."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        default='.', 
        help="The root directory to start scanning from (default: current directory)."
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help="Only list identified dust bunnies, do not suggest cleanup commands."
    )
    parser.add_argument(
        '--suggest-cleanup', 
        action='store_true', 
        help="List identified dust bunnies and suggest cleanup commands."
    )

    args = parser.parse_args()

    print(f"Scanning '{os.path.abspath(args.path)}' for digital dust bunnies...")
    dust_bunnies = find_dust_bunnies(args.path, DEFAULT_PATTERNS)

    if not dust_bunnies:
        print("No digital dust bunnies found! Your repository is sparkling clean. ✨")
        return

    print(f"\nFound {len(dust_bunnies)} digital dust bunnies:\n")
    for bunny_path in dust_bunnies:
        print(f"- {bunny_path}")

    if args.suggest_cleanup:
        print("\nSuggested cleanup commands (review before executing!):\n")
        for bunny_path in dust_bunnies:
            print(generate_cleanup_command(bunny_path))
    elif args.dry_run:
        print("\n(Dry run complete. No cleanup commands suggested.)")


if __name__ == '__main__':
    main()
