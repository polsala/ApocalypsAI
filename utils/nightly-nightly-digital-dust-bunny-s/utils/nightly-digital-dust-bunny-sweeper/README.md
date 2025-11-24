# Nightly Digital Dust Bunny Sweeper

## 🧹 Overview

The `nightly-digital-dust-bunny-sweeper` is a whimsical-yet-practical utility designed to help keep your project repositories sparkling clean. It identifies and optionally removes "digital dust bunnies" – those forgotten, temporary, or unused files and empty directories that accumulate over time, cluttering your workspace and consuming precious disk space.

Think of it as your personal, automated clean-up crew, ready to sweep away the digital debris before it becomes an apocalyptic mess.

## ✨ Features

*   **Pattern-based Scanning**: Configure specific file patterns (e.g., `*.log`, `*.tmp`, `__pycache__`) and directory names to target.
*   **Empty Directory Detection**: Automatically finds and flags empty directories for removal.
*   **Dry Run Mode (Default)**: Safely preview what would be cleaned without making any changes.
*   **Exclusion Paths**: Define paths to ignore during the scan.

## 🚀 Usage

```bash
python src/sweeper.py --path <directory_to_scan> [OPTIONS]
```

### Arguments

*   `--path <directory>`: The root directory to start scanning from. (Required)

### Options

*   `--patterns <pattern1> <pattern2> ...`: Space-separated list of glob patterns for files to identify (e.g., `*.log`, `*.tmp`, `__pycache__`). Default: `['*.log', '*.tmp', '__pycache__', '.DS_Store', 'Thumbs.db']`
*   `--empty-dirs`: Include empty directories in the cleanup scan.
*   `--exclude <path1> <path2> ...`: Space-separated list of paths (files or directories) to explicitly exclude from scanning.
*   `--clean`: **DANGER!** Execute the cleanup, deleting identified files and empty directories. Use with caution after a dry run.
*   `--dry-run`: (Default) Only report what *would* be cleaned, without making any changes. This is overridden by `--clean`.

### Examples

1.  **Dry run to find common junk files and empty directories in the current directory:**
    ```bash
    python src/sweeper.py --path . --empty-dirs
    ```

2.  **Dry run to find specific log files and Python cache directories:**
    ```bash
    python src/sweeper.py --path /my/project --patterns "*.log" "__pycache__"
    ```

3.  **Clean up all identified items (after reviewing a dry run!):**
    ```bash
    python src/sweeper.py --path . --patterns "*.log" "*.tmp" --empty-dirs --clean
    ```

4.  **Exclude a specific directory from the scan:**
    ```bash
    python src/sweeper.py --path . --patterns "*.log" --exclude "data/"
    ```

## 🛠️ Development

The sweeper is written in Python 3.11 and uses standard library modules.
