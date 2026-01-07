A high-performance command-line utility written in Rust for synchronizing files between two directories.

## Features

*   **Fast Synchronization**: Leverages Rust's performance for efficient file copying.
*   **Checksum Verification**: Optional MD5 checksum verification to ensure data integrity.
*   **Dry Run Mode**: Simulate synchronization without making any changes.
*   **Overwrite Control**: Option to overwrite existing files or skip them.

## Installation

Ensure you have Rust and Cargo installed.

```bash
cargo install --git https://github.com/polsala/ApocalypsAI.git --branch main rust-file-sync
```

Or, if you clone the repository:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-rust-file-sync
cargo build --release
```

The executable will be in `target/release/`.

## Usage

```bash
rust-file-sync <source_dir> <destination_dir> [options]
```

### Options

*   `--checksum` or `-c`: Enable MD5 checksum verification for files.
*   `--overwrite` or `-o`: Overwrite existing files in the destination directory.
*   `--dry-run` or `-d`: Perform a dry run, showing what would be synchronized without making changes.
*   `--help` or `-h`: Display help message.

## Examples

Synchronize `~/documents` to `/mnt/backup/documents`:

```bash
rust-file-sync ~/documents /mnt/backup/documents
```

Synchronize with checksum verification and overwrite existing files:

```bash
rust-file-sync ~/documents /mnt/backup/documents -c -o
```

Perform a dry run to see what would be copied:

```bash
rust-file-sync ~/documents /mnt/backup/documents -d
```

## Contributing

Contributions are welcome! Please refer to the main ApocalypsAI repository for contribution guidelines.
