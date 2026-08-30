# Nightly Digital Dust Bunny

A whimsical Node.js CLI utility to help you sweep away your digital dust bunnies – those old, infrequently accessed files that clutter your storage. This tool scans specified directories, identifies files older than a given age, and reports them, helping you declutter your digital space.

## Features

*   **Directory Scanning**: Recursively scans a specified root directory.
*   **Age-based Filtering**: Identifies files older than a configurable number of days based on their last modification time.
*   **Exclusion Patterns**: Allows you to specify regex patterns to ignore certain files or directories (e.g., `node_modules`, `*.log`).
*   **Dry Run Mode**: Preview which files would be identified without making any changes to your file system.
*   **Clear Reporting**: Provides a concise list of identified "dust bunnies" with their modification date and age.

## Installation

To use `nightly-digital-dust-bunny`, you need Node.js (v14 or higher) installed on your system.

You can install it globally via npm:

```bash
npm install -g nightly-digital-dust-bunny
```

Or, if you prefer to use it without global installation:

```bash
npx nightly-digital-dust-bunny <command> [options]
```

## Usage

Run the `digital-dust-bunny` command followed by the path you want to scan and any desired options.

```bash
digital-dust-bunny <path> [options]
```

### Arguments

*   `<path>`: The root directory to start scanning for old files.

### Options

*   `-a, --age <days>`: Minimum age in days for a file to be considered old. Files modified `N` days ago or more will be reported. Defaults to `90`.
*   `-d, --dry-run`: Perform a dry run. The utility will report files but will not suggest any destructive actions (like deletion) and will explicitly state it's a dry run.
*   `-e, --exclude <patterns...>`: Comma-separated regex patterns to exclude files or directories from the scan. For example, `--exclude "node_modules,*.log,temp_files/"`. Can also be provided multiple times, e.g., `--exclude "node_modules" --exclude "*.tmp"`.
*   `-v, --verbose`: Show more detailed output (currently not fully implemented in reporting, but can be expanded).

## Examples

1.  **Scan your current directory for files older than 180 days (dry run):**
    ```bash
digital-dust-bunny . --age 180 --dry-run
    ```

2.  **Scan your 'Documents' folder for files older than 365 days, excluding 'node_modules' and '.git' directories:**
    ```bash
digital-dust-bunny ~/Documents --age 365 --exclude "node_modules,.git"
    ```

3.  **Find all files older than 30 days in a specific project folder:**
    ```bash
digital-dust-bunny /path/to/my/project --age 30
    ```

## Development

To run tests:

```bash
npm test
```

To run the utility directly from the source:

```bash
node src/index.js <path> [options]
```
