# Nightly Data-Dust Sweeper

## Overview
In the post-apocalyptic digital wasteland, even your data caches can accumulate 'data-dust' – old, forgotten, or temporary files that clutter your storage and consume precious resources. The `Nightly Data-Dust Sweeper` is a Node.js CLI utility designed to help survivors keep their digital sanctuaries pristine by identifying and optionally removing these temporal residues.

It allows you to specify a directory and an age threshold (in days). The utility will then list all files older than that threshold, offering a 'dry run' mode for inspection before committing to a 'sweep' (deletion).

## Features
*   **Identify Old Files**: Quickly find files older than a specified number of days.
*   **Dry Run Mode**: Preview which files would be affected without making any changes.
*   **Sweep Mode**: Safely delete identified old files.
*   **Cross-Platform**: Built with Node.js, it runs wherever Node.js is supported.

## Installation
1.  Ensure you have Node.js (v14 or higher) installed.
2.  Navigate to the `nightly-data-dust-sweeper` directory.
3.  Install dependencies (if any, currently none beyond Node.js built-ins):
    ```bash
    npm install
    ```

## Usage

### Dry Run (Default)
To see which files are considered 'data-dust' without deleting anything, simply provide the directory path and the age threshold in days:

```bash
node src/main.js /path/to/your/digital/cache 30
# Example: node src/main.js ./temp_logs 7
```
This will list all files in `/path/to/your/digital/cache` that haven't been modified in the last 30 days.

### Sweep (Delete Files)
To actually remove the identified 'data-dust' files, add the `--sweep` flag:

```bash
node src/main.js /path/to/your/digital/cache 30 --sweep
# Example: node src/main.js /var/log/old_archives 90 --sweep
```
**_WARNING:_** Use the `--sweep` flag with caution. Always perform a dry run first to ensure you are deleting the correct files.

## Development & Testing

To run the automated tests:

```bash
npm test
```

The tests use a mocked file system to ensure determinism and avoid actual file deletions during testing.
