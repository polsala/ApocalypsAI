# Nightly Digital Dust-Bunny Duster

A high-performance CLI tool crafted in Rust to help you unearth and categorize those long-forgotten digital files – your very own "digital dust bunnies." It scans specified directories, identifying files that are both old and large, helping you declutter your digital space with a touch of whimsy.

## Features

*   **High Performance**: Built with Rust for speed and efficiency, ideal for scanning large file systems.
*   **Configurable Criteria**: Define what constitutes a "dust bunny" by setting age and size thresholds.
*   **Human-Readable Output**: Clear, actionable suggestions for managing identified files.
*   **JSON Output**: For integration with other tools or scripting.
*   **Dry Run Mode**: Preview findings without suggesting actions.

## Installation

### Prerequisites

*   Rust toolchain (install via `rustup.rs`)

### Build and Install

1.  Clone the ApocalypsAI repository (or navigate to this utility's directory).
2.  Navigate to the `rust-utils/nightly-digital-dust-duster` directory.
3.  Build the project:
    ```bash
    cargo build --release
    ```
4.  The executable will be located at `target/release/nightly-digital-dust-duster`. You can copy it to a directory in your system's PATH for easy access:
    ```bash
    cp target/release/nightly-digital-dust-duster /usr/local/bin/
    ```

## Usage

```bash
nightly-digital-dust-duster [OPTIONS]
```

### Options

*   `-p, --path <DIR>`: Path to scan for digital dust bunnies. Defaults to the current directory (`.`).
*   `-a, --age <DAYS>`: Files older than N days will be considered dust bunnies. Defaults to `365` days (1 year).
*   `-s, --size <BYTES>`: Files larger than N bytes will be considered dust bunnies. Defaults to `1048576` bytes (1MB).
    *   *Tip*: Use `1024` for KB, `1048576` for MB, `1073741824` for GB.
*   `-d, --dry-run`: Only list files, do not suggest actions.
*   `-f, --format <FORMAT>`: Output format. Can be `human` (default) or `json`.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

### Examples

1.  **Scan the current directory for files older than 2 years and larger than 50MB:**
    ```bash
    nightly-digital-dust-duster --age 730 --size 52428800
    ```

2.  **Scan a specific directory (`~/Documents/OldProjects`) for files older than 90 days and larger than 10MB, in dry-run mode:**
    ```bash
    nightly-digital-dust-duster -p ~/Documents/OldProjects -a 90 -s 10485760 --dry-run
    ```

3.  **Get JSON output for files older than 1 year and larger than 1GB:**
    ```bash
    nightly-digital-dust-duster -a 365 -s 1073741824 --format json
    ```

4.  **Basic scan with default parameters:**
    ```bash
    nightly-digital-dust-duster
    ```

## Development & Testing

To run the tests:

```bash
cargo test
```

The tests create temporary directories and files with specific modification times and sizes to ensure deterministic results, mocking the filesystem interactions.
