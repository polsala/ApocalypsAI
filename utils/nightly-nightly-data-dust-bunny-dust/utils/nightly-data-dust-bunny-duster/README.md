# Nightly Data Dust Bunny Duster

## Overview

The ApocalypsAI Nightly Integrator presents the `nightly-data-dust-bunny-duster`! In the post-apocalyptic digital landscape, data accumulates like dust bunnies under a forgotten server rack. This utility helps you keep your digital bunkers tidy by sniffing out and optionally removing those pesky, useless empty files and directories.

It's like a tiny, diligent robot vacuum for your filesystem, ensuring only valuable data occupies precious storage.

## Features

*   **Empty File Detection**: Identifies files with zero bytes.
*   **Empty Directory Detection**: Locates directories that contain no files or only other empty directories.
*   **Detailed Reporting**: Provides a clear list of all detected 'dust bunnies'.
*   **Safe Dry Run Mode**: Preview what would be deleted without making any changes.
*   **Optional Cleanup**: With confirmation, remove the identified empty files and directories.

## Usage

```bash
python src/duster.py --path <directory_to_scan> [--delete] [--verbose]
```

### Arguments

*   `--path <directory>`: The root directory to start scanning from. **Required.**
*   `--delete`: If provided, the utility will prompt for confirmation before deleting the identified empty files and directories. **Use with caution!**
*   `--verbose`: If provided, print more detailed information during the scan.
*   `--help`: Show the help message and exit.

## Examples

Scan a directory and report:

```bash
python src/duster.py --path ./my_data_hoard
```

Scan a directory and delete after confirmation:

```bash
python src/duster.py --path ./my_temp_files --delete
```

## Installation

This utility is self-contained and requires Python 3.8+.

1.  Navigate to the utility's directory:
    ```bash
    cd utils/nightly-data-dust-bunny-duster
    ```
2.  Run directly:
    ```bash
    python src/duster.py --path /path/to/your/files
    ```

## Development & Testing

To run tests:

```bash
cd utils/nightly-data-dust-bunny-duster
python -m unittest tests/test_duster.py
```
