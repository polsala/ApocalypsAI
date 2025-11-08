# Nightly Digital Dust Bunny Sweeper

## 🧹 What it is

The Nightly Digital Dust Bunny Sweeper is your repository's personal cleaning bot! It's a whimsical-yet-useful utility designed to sniff out and report on the digital 'dust bunnies' that accumulate in your codebase over time. Think of it as a meticulous housekeeper for your files, identifying common temporary files, cache directories, build artifacts, and other digital clutter that can slow down your development environment or bloat your repository.

## ✨ Why it's useful

*   **Repository Hygiene**: Keeps your project directories lean and clean.
*   **Performance**: Reduces the number of files your IDE or build tools need to index/process.
*   **Clarity**: Helps you focus on actual source code by highlighting non-essential files.
*   **Disk Space**: Reclaims precious disk space by identifying large, unnecessary directories.

## 🚀 How to use it

This utility is written in Python and can be run directly from its `src` directory.

1.  **Navigate to the utility**: `cd utils/nightly-digital-dust-bunny-sweeper/src`

2.  **Run a dry-run scan (recommended first!)**: This will list all identified dust bunnies without suggesting any cleanup commands.

    ```bash
    python sweeper.py --path ../../ --dry-run
    ```
    *(The `--path ../../` argument tells it to scan the root of the `polsala/ApocalypsAI` repository. You can specify any path.)*

3.  **Run a scan with suggested cleanup commands**: This will output `rm` or `rd /s /q` commands for the identified items. **Always review these commands before executing them!**

    ```bash
    python sweeper.py --path . --suggest-cleanup
    ```

4.  **Customize patterns**: You can modify the `DEFAULT_PATTERNS` list within `sweeper.py` to include or exclude specific files/directories relevant to your project.

## ⚙️ Configuration (inside `src/sweeper.py`)

The `DEFAULT_PATTERNS` list contains common culprits. Feel free to expand it for your specific needs:

```python
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
```

*Note: This utility focuses on reporting and suggesting cleanup. Always review the output before executing any deletion commands!*
