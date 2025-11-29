# Nightly Echo Chamber Purifier

The Nightly Echo Chamber Purifier is a whimsical-yet-useful utility designed to help you maintain a pristine and efficient file system. It scans a specified directory and its subdirectories for duplicate files, identifying redundant copies that might be cluttering your storage and creating unnecessary "echoes" of data.

By identifying and reporting these duplicates, the Purifier empowers you to make informed decisions about which files to keep, archive, or delete, thereby freeing up valuable disk space and improving system organization.

## How it Works

The utility traverses your file system, calculates a cryptographic hash (MD5, SHA1, or SHA256) for each file, and then groups files by their hash. If multiple files share the same hash, they are considered duplicates. Symbolic links are automatically skipped to prevent infinite loops and ensure only actual file content is compared.

## Installation

This utility is self-contained and written in Python 3.11. No special installation steps or external dependencies (beyond standard Python libraries) are required. Simply place the `nightly-echo-chamber-purifier` folder in your `utils/` directory.

## Usage

To run the Purifier, navigate to the `src` directory within the utility's folder and execute the `purifier.py` script.

```bash
python3 utils/nightly-echo-chamber-purifier/src/purifier.py <path_to_scan> [options]
```

### Arguments

*   `<path_to_scan>`: The starting directory to scan for duplicate files. This is a required argument.

### Options

*   `--hash-algo {md5,sha1,sha256}`: Specifies the hashing algorithm to use.
    *   `md5` (default): Faster, but less collision-resistant.
    *   `sha1`: Slower than MD5, more collision-resistant.
    *   `sha256`: Slowest, but most collision-resistant and recommended for higher security needs.
*   `--exclude <dir1> [<dir2> ...]`: A list of directory names to exclude from the scan. This is useful for skipping common directories like `.git`, `node_modules`, `venv`, etc., to speed up the scan and avoid irrelevant results.

### Examples

1.  **Scan your home directory for duplicates using MD5 (default):**
    ```bash
    python3 utils/nightly-echo-chamber-purifier/src/purifier.py ~/
    ```

2.  **Scan a project directory using SHA256, excluding `.git` and `node_modules`:**
    ```bash
    python3 utils/nightly-echo-chamber-purifier/src/purifier.py /path/to/my/project --hash-algo sha256 --exclude .git node_modules
    ```

3.  **Scan a specific folder for duplicates:**
    ```bash
    python3 utils/nightly-echo-chamber-purifier/src/purifier.py /var/log
    ```

## Output

The utility will print a report to the console, listing each set of duplicate files found, along with their shared hash. If no duplicates are found, it will inform you that your "echo chamber is pure!"

```
Scanning '/path/to/my/project' for duplicate files using SHA256...
Excluding directories: .git, node_modules

Found 2 sets of duplicate files:

Hash: a1b2c3d4e5f6...
  - /path/to/my/project/docs/report_v1.pdf
  - /path/to/my/project/archive/old_report.pdf

Hash: f6e5d4c3b2a1...
  - /path/to/my/project/images/logo.png
  - /path/to/my/project/assets/logo_copy.png

Consider removing redundant files to purify your storage.
```

## Contributing

Feel free to suggest improvements or report issues. The goal is to keep your digital environment as clean and efficient as possible!
