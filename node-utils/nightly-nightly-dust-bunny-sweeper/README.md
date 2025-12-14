# Nightly Digital Dust Bunny Sweeper

A whimsical-yet-useful Node.js CLI utility to help you keep your project directories tidy by identifying and optionally cleaning up old, unused files. Think of those forgotten temporary files, old logs, or build artifacts as 'digital dust bunnies' that accumulate over time.

## Features

*   Recursively scans a specified directory.
*   Identifies files older than a given age threshold.
*   Provides a report of found 'dust bunnies'.
*   Optionally deletes the identified files.

## Installation

1.  **Navigate to the utility directory:**
    ```bash
    cd node-utils/nightly-dust-bunny-sweeper
    ```
2.  **Install dependencies (Jest for testing):**
    ```bash
    npm install
    ```

## Usage

Run the utility from the command line:

```bash
node src/index.js <directory_path> <age_in_days> [--clean]
```

### Arguments:

*   `<directory_path>`: The path to the directory you want to scan (e.g., `./my-project`).
*   `<age_in_days>`: The minimum age (in days) for a file to be considered a 'dust bunny'. Files older than this will be reported.

### Options:

*   `--clean`: (Optional) If provided, the utility will delete the identified 'dust bunny' files. **Use with caution!** Always review the report before cleaning.

### Examples:

1.  **Find files older than 30 days in the current directory (report only):**
    ```bash
    node src/index.js . 30
    ```

2.  **Find and delete files older than 7 days in a specific project folder:**
    ```bash
    node src/index.js /path/to/my/old/project 7 --clean
    ```

3.  **Check for very old files (e.g., 365 days) in your downloads folder:**
    ```bash
    node src/index.js ~/Downloads 365
    ```

## Development & Testing

To run the automated tests:

```bash
npm test
```
