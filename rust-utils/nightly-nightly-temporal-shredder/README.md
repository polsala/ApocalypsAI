# nightly-temporal-shredder

A high-performance CLI tool crafted in Rust to efficiently identify and "shred" (compress and optionally delete) files older than a specified duration. These files are moved to a designated 'temporal void' archive, helping to manage disk space and maintain digital hygiene in the post-apocalyptic data landscape.

## Features

*   **Temporal Decay Logic**: Easily specify a duration (e.g., `7d`, `30m`, `1h`) to target old files.
*   **Efficient Compression**: Utilizes `gzip` for robust and space-saving archiving.
*   **Optional Deletion**: Choose to delete original files after successful shredding.
*   **High Performance**: Built with Rust for speed and memory safety, ideal for large file systems.

## Installation

Ensure you have Rust and Cargo installed. If not, follow the instructions at [rustup.rs](https://rustup.rs/).

```bash
cargo install nightly-temporal-shredder
```

## Usage

```bash
nightly-temporal-shredder <SOURCE_DIRECTORY> <ARCHIVE_DIRECTORY> --older-than <DURATION> [--delete-originals]
```

### Arguments

*   `<SOURCE_DIRECTORY>`: The path to the directory to scan for old files.
*   `<ARCHIVE_DIRECTORY>`: The path where compressed archives will be stored. This directory will be created if it doesn't exist.

### Options

*   `--older-than <DURATION>`: **Required**. Specifies the age threshold for files to be shredded.
    *   Format: `<number><unit>`, e.g., `7d` (7 days), `30m` (30 minutes), `1h` (1 hour).
    *   Supported units: `d` (days), `h` (hours), `m` (minutes), `s` (seconds).
*   `--delete-originals`: If present, the original files will be deleted after successful compression. Use with caution!

### Examples

Shred all files in `/var/log/old` older than 30 days, moving them to `/var/archive/logs` and keeping originals:
```bash
nightly-temporal-shredder /var/log/old /var/archive/logs --older-than 30d
```

Shred files in `/tmp/data` older than 1 hour, moving them to `/tmp/archive` and deleting originals:
```bash
nightly-temporal-shredder /tmp/data /tmp/archive --older-than 1h --delete-originals
```
