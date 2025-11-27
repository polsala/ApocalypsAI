# Nightly Echo Chamber Purifier

## Purpose

The Nightly Echo Chamber Purifier is a standalone utility designed to detect and report duplicate files within specified directories. In a dynamic, autonomous repository like ApocalypsAI, redundant files can accumulate, wasting space and potentially causing confusion. This tool helps maintain a clean and efficient file system by identifying these 'echoes' of data.

It scans files, calculates their content hash (e.g., SHA256), and groups files with identical hashes, presenting them for review. It can be configured to ignore files below a certain size and output results in human-readable text or machine-parseable JSON.

## Usage

Run the `purifier.py` script with one or more paths to scan. Paths can be files or directories.

```bash
python3 src/purifier.py <PATH1> [PATH2 ...] [--hash-algo <algorithm>] [--min-size-kb <size>] [--output-format <format>]
```

### Arguments

*   `<PATH>`: One or more file or directory paths to scan for duplicates.
*   `--hash-algo <algorithm>`: (Optional) Hashing algorithm to use (e.g., `sha256`, `md5`). Defaults to `sha256`. Use `python3 -c 'import hashlib; print(hashlib.algorithms_available)'` to see available algorithms.
*   `--min-size-kb <size>`: (Optional) Minimum file size in kilobytes to consider for hashing. Files smaller than this will be ignored. Defaults to `0` (all files).
*   `--output-format <format>`: (Optional) Output format for duplicates. Can be `text` (default) or `json`.

### Exit Codes

*   `0`: No duplicate files were found.
*   `1`: Duplicate files were found, or an error occurred during execution.

## Examples

1.  **Scan a single directory for duplicates (default settings):**
    ```bash
    python3 src/purifier.py ./my_project_folder
    ```

2.  **Scan multiple paths, using MD5, ignoring files smaller than 5KB:**
    ```bash
    python3 src/purifier.py ./src ./docs /tmp/build_artifacts --hash-algo md5 --min-size-kb 5
    ```

3.  **Output duplicates in JSON format:**
    ```bash
    python3 src/purifier.py ./repository_root --output-format json
    ```

## Development

To run tests, navigate to the `nightly-echo-chamber-purifier` directory and execute:

```bash
python3 -m unittest tests/test_purifier.py
```
