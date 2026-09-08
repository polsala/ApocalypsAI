# nightly-digital-dust-duster

A high-performance Rust CLI tool designed to help you sweep away the digital dust bunnies from your file system. It scans specified directories for files that haven't been accessed or modified in a long time, assigning them a "dustiness" score based on their age. Identify forgotten relics and reclaim valuable storage space!

## Features

*   **Fast Scanning**: Leverages Rust's performance for quick directory traversal.
*   **Configurable Dustiness**: Define what "stale" means to you with a minimum dustiness threshold (in days).
*   **Depth Control**: Limit scanning to a specific directory depth.
*   **Human-Readable Output**: Clearly lists dusty files with their path, size, and dustiness score.

## Installation

Ensure you have Rust and Cargo installed. If not, visit [rust-lang.org](https://www.rust-lang.org/tools/install).

```bash
cargo install nightly-digital-dust-duster
```

## Usage

```bash
nightly-digital-dust-duster [OPTIONS] <PATH>
```

### Arguments

*   `<PATH>`: The root directory to start scanning from.

### Options

*   `-m, --min-dustiness <DAYS>`: Minimum dustiness score (in days) for a file to be reported. Files older than this threshold will be considered "dusty". Default: `30`
*   `-d, --max-depth <DEPTH>`: Maximum depth to traverse into subdirectories. `0` means only the root directory. Default: `unlimited`
*   `-s, --sort-by <FIELD>`: Sort results by 'path', 'size', or 'dustiness'. Default: `dustiness`
*   `-r, --reverse`: Reverse the sort order.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

## Examples

1.  **Find all files older than 90 days in the current directory, sorted by dustiness:**
    ```bash
    nightly-digital-dust-duster . --min-dustiness 90
    ```

2.  **Scan your home directory, but only up to 3 levels deep, for files older than 180 days:**
    ```bash
    nightly-digital-dust-duster ~/ --min-dustiness 180 --max-depth 3
    ```

3.  **List all dusty files (older than 30 days) in `/var/log`, sorted by size (largest first):**
    ```bash
    nightly-digital-dust-duster /var/log --sort-by size --reverse
    ```

## How "Dustiness" is Calculated

The "dustiness" score is the number of days since the file was last accessed or modified, whichever is more recent. A higher score indicates a dustier file.

```
Dustiness (days) = (Current Time - max(Last Access Time, Last Modification Time)) / (24 hours * 60 minutes * 60 seconds)
```

## Contributing

Feel free to contribute to sweeping the digital landscape clean!
