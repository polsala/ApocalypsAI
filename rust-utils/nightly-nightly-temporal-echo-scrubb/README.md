# Nightly Temporal Echo Scrubber

`nightly-temporal-echo-scrubber` is a high-performance Rust CLI tool designed to combat "temporal clutter" in your file systems. It helps you identify and manage old, unused files and directories based on their age and configurable patterns, offering options to perform a dry run, archive them to a dedicated `.temporal_void` directory, or permanently delete them.

## Features

*   **Fast Scanning**: Leverages Rust's performance for quick traversal of large directory structures.
*   **Age-Based Filtering**: Targets files and directories older than a specified number of days.
*   **Pattern Matching**: Supports flexible pattern matching for file names and directory names (e.g., `*.log`, `target/`, `node_modules/`).
*   **Dry Run Mode**: Safely preview changes before execution.
*   **Archiving**: Moves identified "temporal echoes" to a `.temporal_void` directory, preserving their relative paths for potential future recovery.
*   **Deletion**: Permanently removes unwanted clutter.

## Installation

To install `nightly-temporal-echo-scrubber`, you need to have Rust and Cargo installed. If you don't have them, visit [rust-lang.org](https://www.rust-lang.org/tools/install).

```bash
cargo install nightly-temporal-echo-scrubber
```

This will compile and install the `nightly-temporal-echo-scrubber` binary to your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage

```bash
nightly-temporal-echo-scrubber [OPTIONS]
```

### Arguments:

*   `-p, --path <PATH>`: Path to the directory to scan. Defaults to the current directory (`.`).
*   `-a, --age <AGE>`: Age in days. Files/directories older than this will be considered for scrubbing. Defaults to `30` days.
*   `-P, --patterns <PATTERNS>`: Comma-separated list of patterns to match (e.g., `target/,*.log,node_modules/`). Patterns ending with `/` match directories. Wildcards (`*`) are supported at the beginning of file patterns (e.g., `*.bak`).
*   `-d, --dry-run`: Perform a dry run without making any changes. This is highly recommended first.
*   `-A, --archive`: Archive matched items to a `.temporal_void` directory within the scan path. Conflicts with `--delete`.
*   `-D, --delete`: Delete matched items permanently. Conflicts with `--archive`.

### Examples:

1.  **Dry run to see old log files and `target` directories (older than 7 days):**
    ```bash
    nightly-temporal-echo-scrubber --path ./my_project -a 7 -P "*.log,target/" --dry-run
    ```

2.  **Archive all `*.bak` files and `node_modules` directories older than 60 days in the current directory:**
    ```bash
    nightly-temporal-echo-scrubber -a 60 -P "*.bak,node_modules/" --archive
    ```

3.  **Permanently delete `tmp/` directories and `*.temp` files older than 1 day:**
    ```bash
    nightly-temporal-echo-scrubber -a 1 -P "tmp/,*.temp" --delete
    ```

4.  **Scan a specific directory for all files/dirs older than 0 days (i.e., everything not just created):**
    ```bash
    nightly-temporal-echo-scrubber -p /var/log/old_archives -a 0 -P "*" --dry-run
    ```

## Development

To build from source:

```bash
cargo build --release
```

To run tests:

```bash
cargo test
```

## Contributing

Feel free to open issues or pull requests on the ApocalypsAI repository if you have suggestions or bug reports.
