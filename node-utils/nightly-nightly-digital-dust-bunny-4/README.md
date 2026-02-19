# Nightly Digital Dust Bunny Sweeper

## Summary
`nightly-digital-dust-bunny` is a whimsical-yet-useful Node.js command-line interface (CLI) tool designed to help you declutter your digital spaces. It scans specified directories for files that meet certain criteria – being old, unusually large, or matching 'whimsical' patterns (like temporary files or logs) – and lists them as potential 'digital dust bunnies' for your review.

## How it Works
The tool recursively traverses a given directory, collecting metadata (modification time, size, name, extension) for each file. It then applies configurable filters:

*   **Age**: Files older than a specified number of days.
*   **Size**: Files larger than a specified size in kilobytes.
*   **Whimsy Patterns**: Files whose names or extensions match user-defined regular expressions (e.g., `.tmp`, `.log`, `~`, `.bak`, `.DS_Store`).

It outputs a list of identified 'dust bunnies' along with the reasons they were flagged, allowing you to decide on their fate (archival, deletion, or simply ignoring them).

## Installation

1.  **Ensure Node.js is installed**: This utility requires Node.js (v14 or higher).
2.  **Clone the repository (or navigate to the utility's directory)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-digital-dust-bunny
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```
4.  **Make the CLI executable (optional, but recommended for global use)**:
    ```bash
    npm link
    # Now you can run 'dust-bunny' from any directory
    ```
    Alternatively, you can run it directly using `node src/index.js`.

## Usage

Run the `dust-bunny` command followed by the directory you wish to scan and any desired options.

```bash
# Basic scan of the current directory (no filters, will find nothing)
dust-bunny .

# Scan a directory for files older than 30 days
dust-bunny /path/to/my/documents --age 30

# Scan for files larger than 5000 KB (5 MB)
dust-bunny /path/to/downloads --min-size 5000

# Scan for files with whimsical extensions or names (e.g., .log, .tmp, .bak, .DS_Store)
dust-bunny /path/to/project --whimsy-patterns "log,tmp,bak,DS_Store"

# Combine criteria: find files older than 7 days AND larger than 100 KB
dust-bunny /path/to/cache --age 7 --min-size 100

# Combine all criteria and perform a dry run (no deletion suggestions)
dust-bunny /path/to/archive --age 365 --min-size 10240 --whimsy-patterns "old,temp,backup" --dry-run
```

### Options:

*   `-a, --age <days>`: Files older than this many days (based on modification time). (e.g., `--age 30`)
*   `-s, --min-size <kb>`: Files larger than this many kilobytes. (e.g., `--min-size 1024` for 1MB)
*   `-w, --whimsy-patterns <patterns>`: Comma-separated regex patterns for whimsical file names/extensions. (e.g., `--whimsy-patterns "log,tmp,bak,DS_Store"`)
*   `-d, --dry-run`: Perform a dry run. The tool will list files but will not suggest deletion commands, emphasizing review.

## Important Notes

*   **Dry Run is Default**: The tool primarily lists files. It does *not* delete anything directly. For actual deletion, you must use other tools like `rm` or `git clean -fdx` with extreme caution.
*   **Review Carefully**: Always review the list of 'dust bunnies' before taking any action. What's whimsical to one might be critical to another!
*   **Performance**: Scanning very large directories with many files can take some time.

## Development & Testing

To run the automated tests:

```bash
npm test
```
