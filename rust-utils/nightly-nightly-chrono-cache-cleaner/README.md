# Nightly Chrono-Cache Cleaner

A high-performance CLI tool crafted in Rust to help you identify and suggest cleanup for stale or redundant files based on their last access times. It's like a digital dust bunny sweeper for your file system, helping to defragment digital detritus and keep your storage pristine.

## Features

*   **Temporal Echo Detection**: Scans directories for files that haven't been accessed in a specified number of days.
*   **Recursive Scan**: Traverses subdirectories to find hidden digital detritus.
*   **Dry Run Mode**: Preview suggested files without any risk of accidental deletion.
*   **Whimsical Output**: Delivers findings with a touch of ApocalypsAI charm.
*   **Performance**: Built with Rust for speed and efficiency, even on large file systems.

## Installation

To use the Nightly Chrono-Cache Cleaner, you'll need Rust and Cargo installed. If you don't have them, you can get them from [rustup.rs](https://rustup.rs/).

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    # If cloning the whole ApocalypsAI repo
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-chrono-cache-cleaner
    ```
    *(Assuming this utility will be placed under `rust-utils/nightly-chrono-cache-cleaner`)*

2.  **Build the utility:**
    ```bash
    cargo build --release
    ```
    This will compile the cleaner and place the executable in `target/release/`.

3.  **Install (optional, for system-wide access):**
    ```bash
    cargo install --path .
    ```
    This will install `nightly-chrono-cache-cleaner` to your Cargo bin directory, making it available globally.

## Usage

Run the `nightly-chrono-cache-cleaner` command with optional arguments:

```bash
nightly-chrono-cache-cleaner [OPTIONS]
```

### Arguments:

*   `-p`, `--path <PATH>`: The directory path to scan for stale files. Defaults to the current directory (`.`).
*   `-s`, `--stale-days <DAYS>`: The minimum age in days for a file to be considered stale. Files not accessed within this period will be suggested for cleanup. Defaults to `90` days.
*   `-d`, `--dry-run`: Perform a dry run. The tool will identify and list stale files but will not suggest any actions. Useful for previewing.

### Examples:

1.  **Scan the current directory for files older than 90 days (default) in dry run mode:**
    ```bash
    nightly-chrono-cache-cleaner --dry-run
    ```

2.  **Scan a specific directory (`/var/log`) for files older than 30 days:**
    ```bash
    nightly-chrono-cache-cleaner --path /var/log --stale-days 30
    ```

3.  **Get actual suggestions for files older than 180 days in your home directory:**
    ```bash
    nightly-chrono-cache-cleaner -p ~/ -s 180
    ```
    *(Remember to review suggestions carefully before deleting files!)*

## Development & Testing

To run the tests:

```bash
cargo test
```

The tests create temporary files and directories with controlled access times to ensure the cleaner correctly identifies stale files without affecting your actual file system.
