# Digital Dust Bunny Sweeper

## Purpose

The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you tidy up your digital workspace. It identifies and helps you clean up common forms of digital clutter: empty directories and old, temporary-like files (e.g., logs, backups, temporary data).

Think of it as a tiny, autonomous Roomba for your file system, making sure no digital dust bunnies accumulate unnoticed.

## Features

*   **Empty Directory Detection**: Recursively finds and lists directories that contain no files or subdirectories.
*   **Old File Identification**: Locates files older than a specified number of days, optionally filtered by file extensions.
*   **Dry Run Mode**: Always start with `--dry-run` to see what would be cleaned without making any changes.
*   **Configurable**: Specify paths, age thresholds, and file patterns.

## Installation

This utility is self-contained and requires Python 3.8+.

```bash
cd utils/digital-dust-bunny-sweeper
# No special installation needed, just run the script directly.
```

## Usage

Run the `sweeper.py` script from its directory. It accepts several command-line arguments:

```bash
python src/sweeper.py --help
```

**Basic Dry Run (recommended first step):**

This command will scan the current directory (`.`) and its subdirectories, listing all empty directories and files older than 30 days with common temporary extensions, without deleting anything.

```bash
python src/sweeper.py --path . --age-days 30 --extensions .log .tmp .bak .old --dry-run
```

**Performing Cleanup (use with caution!):**

Once you're satisfied with the dry run output, remove the `--dry-run` flag to actually delete the identified clutter.

```bash
python src/sweeper.py --path /path/to/clean --age-days 60 --extensions .log --delete-empty-dirs
```

### Arguments:

*   `--path <directory>`: The root directory to start scanning from. (Required)
*   `--age-days <int>`: Files older than this many days will be considered for deletion. (Default: 30)
*   `--extensions <ext1> <ext2> ...`: Space-separated list of file extensions to target (e.g., `.log .tmp`). If not provided, all files older than `age-days` will be considered.
*   `--delete-empty-dirs`: If present, empty directories found will be deleted. (Use with `--dry-run` first!)
*   `--dry-run`: If present, the script will only list what *would* be deleted, without making any changes.
*   `--verbose`: Print more detailed information during the scan.

## Examples

*   **Find and list all empty directories in your home folder:**
    ```bash
    python src/sweeper.py --path ~/ --delete-empty-dirs --dry-run
    ```
*   **Clean up old build artifacts (e.g., `.o`, `.obj`) in a project directory:**
    ```bash
    python src/sweeper.py --path ./my_project --age-days 90 --extensions .o .obj --dry-run
    ```
*   **Delete all `.log` files older than 7 days in a specific server log directory:**
    ```bash
    python src/sweeper.py --path /var/log/my_app --age-days 7 --extensions .log
    ```

## Contributing

Feel free to contribute to making this digital Roomba even smarter! Open issues for new features or submit pull requests.
