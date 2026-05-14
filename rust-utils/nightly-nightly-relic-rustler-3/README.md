# Nightly Relic Rustler

A high-performance CLI tool to identify and categorize 'relic' files (old, unused data) in specified directories, generating a manifest for cleanup or archival.

## Overview

In the post-apocalyptic digital landscape, data accumulates like dust in forgotten server racks. The `nightly-relic-rustler` helps you sift through the digital detritus, identifying files that are past their prime and might be candidates for archival, deletion, or further investigation. It's your trusty digital metal detector for the data wasteland.

## Features

*   **Fast Scanning**: Leverages Rust's performance for quick directory traversal.
*   **Age-Based Filtering**: Easily specify how old a file must be to be considered a 'relic'.
*   **Categorization**: Attempts to categorize relics by file extension.
*   **Flexible Output**: Generate reports in human-readable text or machine-parseable JSON.

## Installation

To install `nightly-relic-rustler`, you'll need Rust and Cargo installed.

```bash
cargo install relic-rustler
```

Alternatively, clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd rust-utils/nightly-relic-rustler
cargo build --release
./target/release/relic-rustler --help
```

## Usage

```bash
relic-rustler <PATH> [OPTIONS]
```

### Arguments

*   `<PATH>`: The path to the directory you want to scan for relics.

### Options

*   `-a`, `--age <DAYS>`: Minimum age in days for a file to be considered a relic. Files older than this threshold will be reported. (Default: `90`)
*   `-o`, `--output <FORMAT>`: Specify the output format. Can be `text` (default) or `json`.
*   `-h`, `--help`: Print help information.
*   `-V`, `--version`: Print version information.

## Examples

1.  **Scan your `/var/log` directory for files older than 180 days (text output):**

    ```bash
    relic-rustler /var/log --age 180
    ```

2.  **Scan your home directory for files older than a year (365 days) and output as JSON:**

    ```bash
    relic-rustler ~/ --age 365 --output json
    ```

3.  **Find all files older than the default 90 days in a specific data cache:**

    ```bash
    relic-rustler /mnt/data/cache
    ```

## Relic Manifest Output (Text Example)

```
--- Relic Manifest (Older than 90 days) ---
Path: /var/log/old_syslog.1.gz
  Size: 12345 bytes
  Modified: 2023-01-15T10:30:00Z (150 days ago)
  Type: gz

Path: /home/user/documents/forgotten_report.pdf
  Size: 54321 bytes
  Modified: 2022-11-01T14:00:00Z (210 days ago)
  Type: pdf
------------------------------------------
```

## Relic Manifest Output (JSON Example)

```json
[
  {
    "path": "/var/log/old_syslog.1.gz",
    "size_bytes": 12345,
    "modified_at": "2023-01-15T10:30:00Z",
    "age_days": 150,
    "file_type": "gz"
  },
  {
    "path": "/home/user/documents/forgotten_report.pdf",
    "size_bytes": 54321,
    "modified_at": "2022-11-01T14:00:00Z",
    "age_days": 210,
    "file_type": "pdf"
  }
]
```
