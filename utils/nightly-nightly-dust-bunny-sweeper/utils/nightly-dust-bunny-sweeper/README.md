# ApocalypsAI Nightly Dust Bunny Sweeper

## 🧹 What it Does

The Nightly Dust Bunny Sweeper is a whimsical-yet-useful utility designed to keep your project directories sparkling clean. It identifies and removes common digital 'dust bunnies' – temporary files, build artifacts, and cache directories that accumulate over time and clutter your workspace. Think `__pycache__`, `node_modules`, `target/`, `.log` files, and more.

By regularly sweeping these digital remnants, you ensure a leaner repository, faster builds (by forcing fresh ones), and a tidier development environment. It supports a dry-run mode so you can see what would be swept before committing to deletion.

## ✨ Features

*   **Targeted Cleaning**: Removes common build and temporary files/directories across various ecosystems (Python, Node.js, Rust, etc.).
*   **Configurable Patterns**: Use default patterns or provide your own to customize what gets swept.
*   **Dry Run Mode**: Preview all identified 'dust bunnies' without making any changes.
*   **Recursive Scan**: Scans subdirectories from a specified root path.
*   **Self-Contained**: A single Python script with no external dependencies beyond standard library modules.

## 🚀 Usage

To run the Dust Bunny Sweeper, navigate to your project's root directory or specify a path.

```bash
# Navigate to the utility's directory first (or add it to your PATH)
cd utils/nightly-dust-bunny-sweeper

# Run a dry-run to see what would be deleted in the current directory
python src/sweeper.py --dry-run

# Run a dry-run for a specific path
python src/sweeper.py /path/to/your/project --dry-run

# Actually sweep the dust bunnies in the current directory
# BE CAREFUL: This will delete files and directories!
python src/sweeper.py

# Sweep dust bunnies in a specific directory with custom patterns
python src/sweeper.py /path/to/another/project --patterns "*.tmp" "old_builds" "temp_data/"
```

### Arguments

*   `<path>` (optional): The root directory to start sweeping from. Defaults to the current directory (`.`).
*   `--dry-run`: Perform a dry run. The utility will list all files and directories it *would* delete, but won't actually remove anything.
*   `--patterns <pattern1> <pattern2> ...`: Override the default list of patterns. Provide space-separated patterns. Wildcards (`*`) are supported for file names (e.g., `*.log`, `*.tmp`). Exact names are used for directories (e.g., `__pycache__`, `node_modules`).

## ⚙️ Default Patterns

By default, the sweeper looks for the following:

*   `__pycache__`
*   `target` (Rust build directory)
*   `node_modules`
*   `build`
*   `dist`
*   `.pytest_cache`
*   `.mypy_cache`
*   `.DS_Store`
*   `*.pyc`
*   `*.log`
