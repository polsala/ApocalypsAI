# Cosmic Dust Bunny Sweeper

## 🧹 What is this?

In the vast cosmos of your project directory, digital 'dust bunnies' accumulate: temporary files, empty directories, forgotten build artifacts, and other detritus. The Cosmic Dust Bunny Sweeper is here to help! It's a whimsical-yet-useful utility designed to identify and sweep away these digital remnants, ensuring your workspace remains pristine and free of unnecessary clutter.

Think of it as a tiny, automated janitor for your file system, preventing entropy from taking over your precious project space.

## ✨ Features

*   **Configurable Patterns**: Define which file names, extensions, or directory names constitute a 'dust bunny'.
*   **Empty Directory Detection**: Automatically finds and removes directories that have become barren.
*   **Dry Run Mode**: See exactly what would be swept away before any actual deletion occurs.
*   **Recursive Cleaning**: Scans subdirectories to ensure no dust bunny is left unturned.

## 🚀 Usage

To run the sweeper, navigate to its directory and execute the Python script. It's designed to be self-contained.

```bash
cd utils/cosmic-dust-bunny-sweeper/src
python sweeper.py <target_directory> [--patterns <pattern1> <pattern2> ...] [--no-dry-run]
```

### Arguments:

*   `<target_directory>`: The root directory to start sweeping from. (e.g., `.` for current directory)
*   `--patterns`: (Optional) A space-separated list of glob-style patterns (e.g., `*.tmp`, `__pycache__`, `.DS_Store`). If not provided, a default set of common patterns will be used.
*   `--no-dry-run`: (Optional) By default, the sweeper runs in dry-run mode, only printing what it *would* delete. Use this flag to perform actual deletions.

### Example:

To see what would be cleaned in the current directory, using default patterns:

```bash
python sweeper.py .
```

To actually clean up `__pycache__` directories and `.log` files in your `my_project` folder:

```bash
python sweeper.py ../../my_project --patterns __pycache__ *.log --no-dry-run
```

## ⚙️ Default Patterns

If no `--patterns` are specified, the sweeper will look for:

*   `__pycache__` directories
*   `.DS_Store` files
*   `*.tmp` files
*   `*.log` files
*   `*.bak` files
*   `Thumbs.db` files
*   `*.swp` (Vim swap files)
*   `*.swo` (Vim swap files)
*   `*.pyc` files
*   Empty directories

## ⚠️ Caution

Always use the dry-run mode first to review the proposed deletions. While designed to be safe, directly deleting files can lead to data loss if patterns are too broad or incorrectly applied. Use `--no-dry-run` with care!
