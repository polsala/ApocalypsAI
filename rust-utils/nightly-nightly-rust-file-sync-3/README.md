# nightly-rust-file-sync

A whimsical yet useful standalone utility for synchronizing files between two directories. Built with Rust for performance and reliability.

## Features

*   **Fast Synchronization**: Leverages Rust's performance to quickly copy and update files.
*   **Dry Run**: Simulate synchronization without making any actual changes.
*   **Verbose Output**: See detailed information about which files are being copied or updated.
*   **Error Handling**: Robust error reporting for file operations.

## Installation

To build and install this utility, you'll need Rust and Cargo installed.

1.  Clone the repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```

2.  Navigate to the utility's directory:
    ```bash
    cd rust-utils/nightly-rust-file-sync
    ```

3.  Build the project:
    ```bash
    cargo build --release
    ```

4.  The executable will be in `target/release/nightly-rust-file-sync`. You can copy it to your PATH or run it directly.

## Usage

```bash
nightly-rust-file-sync <source_dir> <destination_dir> [options]
```

### Arguments

*   `source_dir`: The directory to copy files from.
*   `destination_dir`: The directory to copy files to.

### Options

*   `-d`, `--dry-run`: Perform a trial run with no changes made.
*   `-v`, `--verbose`: Enable verbose output, showing each file operation.
*   `-h`, `--help`: Print help information.

## Examples

Synchronize `~/my_documents` to `/backup/documents`:

```bash
nightly-rust-file-sync ~/my_documents /backup/documents
```

Perform a dry run to see what would be synchronized:

```bash
nightly-rust-file-sync ~/my_documents /backup/documents --dry-run
```

Synchronize with verbose output:

```bash
nightly-rust-file-sync ~/my_documents /backup/documents -v
```
