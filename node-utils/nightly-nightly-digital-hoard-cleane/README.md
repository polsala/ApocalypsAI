# Nightly Digital Hoard Cleaner

A whimsical utility to help you manage your digital clutter by identifying and optionally cleaning up old, forgotten files (your "digital hoard") in specified directories. Think of it as a friendly digital dust bunny sweeper, helping you keep your file system sparkling clean or moving ancient artifacts to a "compost pile" for later review.

## Features

*   **Age-based Cleanup**: Target files older than a specified number of days.
*   **Dry Run Mode**: Preview which files would be affected without making any changes.
*   **Compost Pile**: Instead of permanent deletion, move old files to a designated "compost" directory.
*   **Recursive Scan**: Optionally scan subdirectories for hidden digital treasures.
*   **Cross-Platform**: Built with Node.js, runs on Windows, macOS, and Linux.

## Installation

This is a standalone Node.js script. No `npm install` is strictly required if you have Node.js installed.

1.  **Ensure Node.js is installed**: Download from [nodejs.org](https://nodejs.org/).
2.  **Save the files**: Place `src/index.js` and `README.md` in a directory, e.g., `nightly-digital-hoard-cleaner/`.

## Usage

Navigate to the utility's directory and run it using `node`:

```bash
node src/index.js [options]
```

### Options

*   `-d, --dir <path>`: Directory to clean (default: current working directory).
*   `-a, --age <days>`: Files older than this many days will be targeted (default: 30).
*   `-n, --dry-run`: Only list files, do not move or delete them.
*   `-c, --compost <path>`: Move old files to this directory instead of deleting them.
*   `-r, --recursive`: Scan subdirectories recursively.
*   `-h, --help`: Display this help message.

### Examples

1.  **Dry run to see files older than 60 days in the current directory:**
    ```bash
    node src/index.js --age 60 --dry-run
    ```

2.  **Move files older than 90 days from `/path/to/my/downloads` to a `/tmp/digital-compost` directory:**
    ```bash
    node src/index.js --dir /path/to/my/downloads --age 90 --compost /tmp/digital-compost
    ```

3.  **Recursively delete files older than 7 days in your project's `dist` folder:**
    ```bash
    node src/index.js --dir ./my-project/dist --age 7 --recursive
    ```

4.  **Display help:**
    ```bash
    node src/index.js --help
    ```

## Development & Testing

To run the tests, navigate to the utility's directory and execute the test file directly with Node.js:

```bash
node tests/index.test.js
```

The tests use Node.js's built-in `assert` module and mock the `fs.promises` module to ensure deterministic and offline execution without touching the actual file system.
