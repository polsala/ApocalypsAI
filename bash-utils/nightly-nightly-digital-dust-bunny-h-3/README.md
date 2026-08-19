# Nightly Digital Dust Bunny Hunt

## 🌌 Overview

Welcome, weary traveler of the digital wastes! Is your system feeling sluggish? Are ancient, forgotten files accumulating like radioactive fallout? Fear not! The `nightly-digital-dust-bunny-hunt` is here to help you unearth and sweep away those pesky 'digital dust bunnies' – old, unused files that clutter your precious storage.

This whimsical Bash script scans a specified directory for files older than a certain age and offers an interactive cleanup. It's like a post-apocalyptic Roomba for your filesystem!

## ✨ Features

*   **Whimsical Narrative**: Enjoy a lighthearted, themed experience while performing system maintenance.
*   **Configurable Scan**: Specify the directory to scan and the age threshold for files.
*   **Interactive Cleanup**: Review detected 'dust bunnies' and choose whether to sweep them away.
*   **Dry Run Mode**: See what would be cleaned without actually deleting anything.

## 🚀 Usage

### Prerequisites

*   Bash shell
*   `find` utility
*   `rm` utility
*   `xargs` utility

### Running the Hunt

Navigate to the `src` directory and execute the script:

```bash
./src/dust_bunny_hunt.sh [SCAN_DIRECTORY] [AGE_IN_DAYS] [--dry-run]
```

*   `[SCAN_DIRECTORY]` (optional): The directory to scan for old files. Defaults to `/tmp` if not provided.
*   `[AGE_IN_DAYS]` (optional): Files older than this many days will be considered 'dust bunnies'. Defaults to `7` days if not provided.
*   `--dry-run` (optional): If present, the script will only report what *would* be deleted, without actually performing any cleanup.

### Examples

1.  **Scan `/tmp` for files older than 7 days (default behavior):**
    ```bash
    ./src/dust_bunny_hunt.sh
    ```

2.  **Scan `/var/log` for files older than 30 days:**
    ```bash
    ./src/dust_bunny_hunt.sh /var/log 30
    ```

3.  **Perform a dry run scan on your home directory for files older than 90 days:**
    ```bash
    ./src/dust_bunny_hunt.sh ~/ 90 --dry-run
    ```

## ⚠️ Important Notes

*   **Use with Caution**: While whimsical, this script can delete files. Always understand what you're deleting, especially when running it on critical directories. The `--dry-run` option is your friend!
*   **Permissions**: Ensure the script has the necessary permissions to read and delete files in the target directory.

## 🧹 May your digital realm be ever clean!
