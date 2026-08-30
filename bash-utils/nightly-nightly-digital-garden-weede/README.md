# Nightly Digital Garden Weeder

## 🌿 Overview

The `nightly-digital-garden-weeder` is a whimsical Bash script designed to help you maintain a pristine digital environment. It acts as a diligent gardener, identifying and offering to prune "ancient digital weeds" (files older than a specified age) and "desolate empty plots" (empty directories) from your filesystem. Keep your digital garden flourishing and free from clutter!

## ✨ Features

*   **Age-based File Pruning**: Finds and lists files older than a configurable number of days.
*   **Empty Directory Reclamation**: Identifies and lists empty directories.
*   **Dry Run Mode**: Preview changes without actually deleting anything.
*   **Interactive Confirmation**: Prompts for confirmation before deletion (can be skipped).
*   **Whimsical Messaging**: Enjoy delightful messages as your garden is tended.

## 🚀 Usage

To run the Digital Garden Weeder, execute the `weeder.sh` script with your desired options.

```bash
./src/weeder.sh [OPTIONS]
```

### Options

*   `-p, --path <path>`: Specify the root path of your digital garden (default: current directory `.`)
*   `-a, --age <days>`: Files older than this many days will be considered weeds (default: `30`)
*   `-d, --dry-run`: Perform a dry run without making any actual changes.
*   `-y, --confirm`: Automatically confirm deletion without an interactive prompt.
*   `-h, --help`: Display the help message.

### Examples

1.  **Dry run to see old files and empty directories in your home directory (older than 60 days):**
    ```bash
    ./src/weeder.sh --path ~/ --age 60 --dry-run
    ```

2.  **Clean up temporary files in `/tmp` older than 7 days, with automatic confirmation:**
    ```bash
    ./src/weeder.sh -p /tmp -a 7 -y
    ```

3.  **Interactively clean up your Downloads folder, pruning files older than 90 days:**
    ```bash
    ./src/weeder.sh --path ~/Downloads --age 90
    ```

## 🛠️ Development

### Running Tests

The utility includes a self-contained test script that uses mock functions for `find` and `rm` to ensure deterministic and offline testing.

```bash
./tests/test_weeder.sh
```

This will execute a series of tests to verify the script's behavior in various scenarios (dry runs, deletions, cancellations, error handling) without affecting your actual filesystem.
