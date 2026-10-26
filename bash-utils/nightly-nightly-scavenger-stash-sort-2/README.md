# Nightly Scavenger's Stash Sorter

A whimsical yet practical bash utility for organizing your digital "finds" (files) into categorized subdirectories, much like a diligent scavenger sorting their precious loot in the wasteland. Keep your digital hoard tidy and accessible!

## Features

*   **Categorized Sorting**: Automatically moves files based on their extensions into predefined categories (e.g., `documents`, `images`, `archives`, `executables`, `audio`, `video`, `code`, `other_finds`).
*   **Dry Run Mode**: Preview what the script will do without actually moving any files.
*   **Idempotent**: Can be run multiple times on the same directory without issues.
*   **Safe**: Only moves files; does not delete anything unless explicitly configured (not in this version).

## Usage

```bash
./nightly-scavenger-stash-sort.sh [OPTIONS] <source_directory>
```

### Arguments

*   `<source_directory>`: The path to the directory whose contents you want to sort.

### Options

*   `-d`, `--dry-run`: Perform a dry run. The script will print what it *would* do without making any changes.
*   `-h`, `--help`: Display this help message.

## Examples

1.  **Sort files in the current directory (dry run):**
    ```bash
    ./nightly-scavenger-stash-sort.sh --dry-run .
    ```

2.  **Sort files in a specific download folder:**
    ```bash
    ./nightly-scavenger-stash-sort.sh /home/user/Downloads
    ```

3.  **Sort files in a temporary cache directory:**
    ```bash
    ./nightly-scavenger-stash-sort.sh /tmp/my_cache
    ```

## Categories & Extensions

The script currently recognizes the following categories:

*   **documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.md`, `.csv`, `.xls`, `.xlsx`, `.ppt`, `.pptx`
*   **images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.svg`
*   **archives**: `.zip`, `.tar`, `.gz`, `.bz2`, `.xz`, `.rar`, `.7z`
*   **executables**: `.sh`, `.run`, `.bin`
*   **audio**: `.mp3`, `.wav`, `.aac`, `.flac`, `.ogg`
*   **video**: `.mp4`, `.mkv`, `.avi`, `.mov`, `.webm`
*   **code**: `.py`, `.js`, `.ts`, `.html`, `.css`, `.json`, `.xml`, `.yml`, `.yaml`, `.go`, `.rs`, `.java`, `.c`, `.cpp`, `.h`, `.hpp`
*   **other_finds**: Any file not matching the above categories.

## Development & Testing

The utility includes a self-contained test script (`tests/test_nightly-scavenger-stash-sort.sh`) that uses temporary directories and files to ensure functionality without affecting your system.
