# Nightly Digital Dust Bunny Sweeper

## 🧹 Overview

The Nightly Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to keep your repository pristine by automatically identifying and removing common temporary files, build artifacts, and cache directories. Think of it as a diligent digital janitor, sweeping away the "dust bunnies" that accumulate in your project over time, freeing up space and reducing clutter.

It's particularly useful for CI/CD pipelines or nightly maintenance tasks to ensure a clean slate for builds or to reduce the size of archives.

## ✨ Features

*   **Targeted Cleanup**: Removes files and directories matching predefined patterns.
*   **Customizable**: Easily extend or override the default patterns to suit your project's needs.
*   **Dry Run Mode**: Preview what would be deleted without actually removing anything.
*   **Recursive**: Cleans up within subdirectories.

## 🚀 Usage

### Command Line

To run the sweeper from the command line:

```bash
python src/sweeper.py --path /path/to/your/repo [--dry-run] [--patterns "pattern1" "pattern2"]
```

*   `--path <directory>`: The root directory to start sweeping from. **Required.**
*   `--dry-run`: If present, the utility will only print what *would* be deleted, without performing any actual deletions.
*   `--patterns <pattern1> <pattern2> ...`: A space-separated list of additional patterns to include. These patterns will be added to the default list. For example: `--patterns "*.log" "temp_dir"`.

### Default Patterns

The sweeper targets the following common "dust bunnies" by default:

*   `__pycache__` (Python cache directories)
*   `*.pyc` (Compiled Python files)
*   `*.pyo` (Optimized Python files)
*   `.DS_Store` (macOS specific metadata files)
*   `node_modules` (Node.js dependency directories)
*   `dist` (Common build output directories)
*   `build` (Common build output directories)
*   `target` (Java/Rust build output directories)
*   `.vscode` (VS Code configuration directories)
*   `.idea` (IntelliJ IDEA configuration directories)
*   `*.log` (Log files)
*   `*.tmp` (Temporary files)
*   `*.bak` (Backup files)

## 🛠️ Development

### Running Tests

To ensure the sweeper is doing its job correctly, run the tests:

```bash
python -m unittest tests/test_sweeper.py
```
