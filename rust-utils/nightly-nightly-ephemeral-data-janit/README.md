# Nightly Ephemeral Data Janitor

## Overview

The `nightly-ephemeral-data-janitor` is a whimsical Rust CLI tool designed to help you tidy up your digital workspace by sweeping away old, ephemeral files and 'digital dust bunnies'. It scans specified directories for files older than a given duration and offers to either list them (dry run) or permanently remove them.

Think of it as a friendly digital custodian, ensuring your directories remain sparkling clean and free from forgotten data.

## Features

*   **Age-based Deletion**: Identify and remove files older than a specified duration.
*   **Recursive Scanning**: Traverses directories recursively to find hidden digital clutter.
*   **Dry Run Mode**: Preview which files would be affected before making any changes.
*   **Whimsical Output**: Enjoy charming messages as your digital space gets tidied.
*   **Performance**: Built with Rust for speed and efficiency in file system operations.

## Installation

To install `nightly-ephemeral-data-janitor`, you'll need Rust and Cargo installed on your system. If you don't have them, visit [rustup.rs](https://rustup.rs/) for instructions.

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-ephemeral-data-janitor
    ```
2.  **Build and install:**
    ```bash
    cargo install --path .
    ```
    This will install the `nightly-ephemeral-data-janitor` executable to your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage

```bash
nightly-ephemeral-data-janitor [OPTIONS] <PATHS>...
```

### Arguments

*   `<PATHS>...`: One or more directories to scan for ephemeral files.

### Options

*   `-a, --age <DURATION>`: The maximum age for files to be considered ephemeral. Files older than this duration will be targeted. Format: `"<N>d"` for days, `"<N>h"` for hours, `"<N>m"` for minutes. E.g., `"7d"`, `"24h"`, `"30m"`. (Default: `"7d"`)
*   `-d, --dry-run`: Perform a dry run. List files that would be deleted without actually removing them.
*   `-v, --verbose`: Enable verbose output, showing more details about scanned files.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

### Examples

1.  **Dry run, listing files older than 30 days in the current directory and `/tmp`:**
    ```bash
    nightly-ephemeral-data-janitor --dry-run --age "30d" . /tmp
    ```

2.  **Delete files older than 24 hours in `~/Downloads` (use with caution!):**
    ```bash
    nightly-ephemeral-data-janitor --age "24h" ~/Downloads
    ```

3.  **List verbose details for files older than 1 hour in a specific project cache directory:**
    ```bash
    nightly-ephemeral-data-janitor --dry-run --verbose --age "1h" ./my_project/.cache
    ```

## Contributing

Contributions are welcome! Feel free to open issues or pull requests on the main ApocalypsAI repository.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
