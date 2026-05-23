# Nightly Digital Debris Collector

`nightly-digital-debris-collector` is a high-performance Rust CLI tool designed to help you reclaim your digital wasteland by identifying 'digital debris' – files and directories that are old, unusually small, or completely empty.

Think of it as your personal byte-dust sweeper, helping you find forgotten relics and digital detritus that might be cluttering your storage.

## Features

*   **Fast Scanning:** Leverages Rust's performance for quick directory traversal.
*   **Configurable Criteria:** Define what constitutes 'debris' based on age, size, and emptiness.
*   **Dry Run:** Safely inspect potential debris without making any changes.
*   **Human-Readable Output:** Clear, concise reports for easy understanding.
*   **JSON Output:** Programmatic output for integration with other tools.

## Installation

To install `nightly-digital-debris-collector`, you'll need Rust and Cargo installed. If you don't have them, visit [rustup.rs](https://rustup.rs/).

```bash
cargo install nightly-digital-debris-collector
```

Alternatively, clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-digital-debris-collector
cargo build --release
# The executable will be in target/release/nightly-digital-debris-collector
```

## Usage

```bash
nightly-digital-debris-collector [OPTIONS] <PATH>
```

### Arguments

*   `<PATH>`: The root directory to start scanning from. Defaults to the current directory if not specified.

### Options

*   `-a, --age <DAYS>`: Files/directories older than this many days are considered debris. Default: `365`.
*   `-s, --size <BYTES>`: Files smaller than this many bytes are considered debris. Default: `1024` (1KB).
*   `-e, --empty-dirs`: Include empty directories in the debris report. By default, only files are considered for size/age.
*   `-j, --json`: Output the report in JSON format.
*   `-v, --verbose`: Show more detailed scanning progress.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

### Examples

1.  **Scan current directory for debris older than 2 years (730 days) or smaller than 500 bytes:**

    ```bash
    nightly-digital-debris-collector . --age 730 --size 500
    ```

2.  **Scan a specific directory, including empty directories, and output as JSON:**

    ```bash
    nightly-digital-debris-collector /var/log/old_archives --empty-dirs --json
    ```

3.  **Find all files older than 30 days in your home directory:**

    ```bash
    nightly-digital-debris-collector ~/ --age 30
    ```

## Output Format

### Human-Readable (Default)

```
Scanning for byte-dust in "/path/to/scan"...

Found a forgotten relic:
  Path: /path/to/scan/old_log.txt
  Type: File
  Reason: Older than 365 days (Last modified: 2022-01-15)

Digital detritus identified:
  Path: /path/to/scan/tiny_config.cfg
  Type: File
  Reason: Smaller than 1024 bytes (Size: 128 bytes)

Empty void detected:
  Path: /path/to/scan/empty_folder/
  Type: Directory
  Reason: Is empty

Reclamation complete. Total debris items found: 3.
```

### JSON Output (`--json`)

```json
[
  {
    "path": "/path/to/scan/old_log.txt",
    "type": "file",
    "reason": "older_than_age",
    "details": {
      "last_modified": "2022-01-15T10:30:00Z",
      "age_days": 730
    }
  },
  {
    "path": "/path/to/scan/tiny_config.cfg",
    "type": "file",
    "reason": "smaller_than_size",
    "details": {
      "size_bytes": 128,
      "threshold_bytes": 1024
    }
  },
  {
    "path": "/path/to/scan/empty_folder",
    "type": "directory",
    "reason": "is_empty"
  }
]
```
