# ApocalypsAI Nightly Digital Dust Bunny Sweeper

The digital wasteland can accumulate quite a bit of forgotten debris — empty directories, ancient log files, and other digital dust bunnies. The `nightly-digital-dust-bunny-sweeper` is here to help you tidy up your digital shelters, identifying and optionally sweeping away these forgotten remnants.

## 🗑️ What it Does

This utility scans a specified directory recursively to find:
- **Empty Directories**: Folders that contain no files or subdirectories.
- **Ancient Files**: Files that haven't been modified in a specified number of days (default: 30 days).

It provides a report of these "dust bunnies" and, if you choose, can automatically delete them.

## 🚀 Usage

### Prerequisites

- Node.js (v14 or higher)

### Installation

1.  Navigate to the `node-utils/nightly-digital-dust-bunny-sweeper` directory.
2.  Install development dependencies (like Jest for testing):
    ```bash
    npm install
    ```

### Running the Sweeper

```bash
node src/index.js <path_to_scan> [--sweep] [--max-age <days>]
```

-   `<path_to_scan>`: The absolute or relative path to the directory you want to scan.
-   `--sweep`: (Optional) Add this flag to actually delete the identified empty directories and ancient files. **Use with caution!** Without this flag, the utility will only report its findings (dry run).
-   `--max-age <days>`: (Optional) Specify the maximum age in days for a file to be considered "ancient". Files older than this will be flagged. Defaults to 30 days.

#### Examples:

1.  **Dry Run (Report Only)**: Scan your `~/Downloads` directory for empty folders and files older than 30 days.
    ```bash
    node src/index.js ~/Downloads
    ```

2.  **Dry Run with Custom Age**: Scan `/var/log` for empty folders and files older than 7 days.
    ```bash
    node src/index.js /var/log --max-age 7
    ```

3.  **Sweep (Delete)**: Scan your `~/temp` directory and delete all identified empty folders and files older than 30 days.
    ```bash
    node src/index.js ~/temp --sweep
    ```

## 🧪 Tests

To run the tests:

1.  Ensure you have installed dependencies:
    ```bash
    npm install
    ```
2.  Run the tests:
    ```bash
    npm test
    ```

The tests use mocks for `fs.promises` to ensure they are deterministic and do not interact with the actual file system.
