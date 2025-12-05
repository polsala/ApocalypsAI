# Chronos Cache Cleaner

## ⏳ Sweep Away the Temporal Dust Bunnies!

In the ever-accelerating march of time, our digital workspaces accumulate forgotten files, ancient logs, and temporary detritus. The Chronos Cache Cleaner is your trusty digital broom, designed to help you identify and purge these temporal anomalies, keeping your filesystem lean, mean, and ready for the next apocalypse (or just your next coding session).

This utility provides a simple command-line interface to scan a specified directory, pinpoint files and folders older than a given threshold, and either report them or delete them.

## ✨ Features

*   **Age-based Cleanup**: Target files and directories older than a specified number of days.
*   **Pattern Matching**: Include or exclude files based on glob patterns (e.g., `*.log`, `temp/`).
*   **Dry Run Mode**: Safely preview what *would* be deleted without making any changes.
*   **Recursive Scan**: Thoroughly inspect subdirectories for hidden relics.

## 🚀 Installation

This utility is self-contained and written in Python 3.x. No special installation steps are required beyond having a compatible Python interpreter.

1.  Navigate to the `utils/chronos-cache-cleaner/` directory.
2.  Run the `cleaner.py` script directly.

## 💡 Usage

```bash
python src/cleaner.py --path <directory_to_scan> [OPTIONS]
```

### Arguments

*   `--path <directory>`: **(Required)** The root directory to start scanning from.
*   `--age-days <int>`: **(Required)** Files/directories older than this many days will be considered for cleaning. (e.g., `30` for 30 days).
*   `--dry-run`: **(Default)** Perform a dry run. List files/directories that *would* be deleted without actually deleting them. This is the safest mode.
*   `--delete`: **(DANGER!)** Actually delete the identified files and directories. Use with extreme caution and after reviewing a dry run.
*   `--include <pattern>`: One or more glob patterns to *include* files/directories. Only items matching these patterns will be considered. Can be specified multiple times. (e.g., `--include "*.log" --include "temp_dir/*")
*   `--exclude <pattern>`: One or more glob patterns to *exclude* files/directories. Items matching these patterns will be ignored, even if they are old. Can be specified multiple times. (e.g., `--exclude "important_data/*" --exclude "*.bak")

### Examples

1.  **Dry run: Find all files/dirs older than 90 days in your home directory:**
    ```bash
    python src/cleaner.py --path ~/ --age-days 90 --dry-run
    ```

2.  **Delete old log files (`*.log`) and temporary directories (`temp_*`) older than 7 days in a project folder:**
    ```bash
    python src/cleaner.py --path ./my_project/ --age-days 7 --include "*.log" --include "temp_*" --delete
    ```

3.  **Dry run: Find all old files/dirs, but exclude anything in a `node_modules` folder:**
    ```bash
    python src/cleaner.py --path ./my_repo/ --age-days 180 --exclude "node_modules/*" --dry-run
    ```

## ⚠️ Important Notes

*   **Always start with `--dry-run`!** Review the output carefully before using `--delete`.
*   Deletion is permanent. There is no undo.
*   Be mindful of the `--path` you provide. Cleaning your root directory (`/`) without careful `--exclude` patterns is highly discouraged.
