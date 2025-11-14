# Nightly Cosmic Dust Collector

## Purpose

The Nightly Cosmic Dust Collector is a whimsical utility designed to help maintain a clean and tidy repository by identifying and optionally 'collecting' (moving) stale files and removing empty directories. Think of it as a celestial janitor, sweeping away the accumulated cosmic dust of forgotten files and vacant spaces.

It's particularly useful for development environments, build artifacts, or temporary files that tend to accumulate over time, ensuring your project space remains pristine and focused.

## Usage

Run the `dust_collector.py` script from the command line. It requires a target path and an age threshold for files.

```bash
python src/dust_collector.py <target_path> [--age <days>] [--dry-run] [--dust-bin-name <name>]
```

### Arguments:

*   `<target_path>`: The root directory to scan for cosmic dust.
*   `--age <days>`: (Optional) The minimum age in days for a file to be considered 'stale'. Files older than this will be flagged. Defaults to `30` days.
*   `--dry-run`: (Optional) If present, the utility will only report what it *would* do, without making any changes to the filesystem. Highly recommended for initial runs.
*   `--dust-bin-name <name>`: (Optional) The name of the directory where stale files will be moved. This directory will be created at the root of the `target_path`. Defaults to `.cosmic-dust-bin`.

### Examples:

1.  **Dry run, reporting stale files older than 60 days in the current directory:**
    ```bash
    python src/dust_collector.py . --age 60 --dry-run
    ```

2.  **Collect stale files (older than 30 days) and remove empty directories in a specific project folder:**
    ```bash
    python src/dust_collector.py /path/to/my/project
    ```

3.  **Collect stale files into a custom 'archive' folder:**
    ```bash
    python src/dust_collector.py . --dust-bin-name .archive-old-files
    ```

## Output

The utility will print a summary of identified stale files and empty directories. In non-dry-run mode, it will also report on the actions taken (files moved, directories removed).

## How it Works

1.  **Scans**: Recursively traverses the specified `target_path`.
2.  **Identifies Stale Files**: Checks the last modification time of each file. If a file's age exceeds the `--age` threshold, it's marked as stale.
3.  **Identifies Empty Directories**: After processing files, it identifies directories that contain no files or subdirectories.
4.  **Collects Dust (Non-Dry Run)**:
    *   Creates a `.cosmic-dust-bin` (or custom named) directory at the root of the `target_path` if it doesn't exist.
    *   Moves all identified stale files into this dust bin.
    *   Removes all identified empty directories.

This process ensures that no data is permanently deleted without explicit action, as stale files are merely relocated.
