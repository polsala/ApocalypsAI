# Nightly Data Debris Duster

## Overview
In the post-apocalyptic digital wasteland, storage space is a precious commodity. The `nightly-data-debris-duster` is a high-performance Rust CLI tool designed to help you reclaim valuable bytes by identifying and reporting duplicate files within a specified directory. It recursively scans, calculates SHA256 hashes, and presents a clear list of all identical 'data debris' that can be safely removed.

Think of it as a digital broom, sweeping away the redundant remnants of forgotten data caches.

## Features
*   **High Performance**: Written in Rust for speed and efficiency.
*   **Recursive Scanning**: Traverses subdirectories to find all files.
*   **SHA256 Hashing**: Uses cryptographic hashes to reliably identify identical file content.
*   **Clear Reporting**: Outputs groups of duplicate files with their shared hash.
*   **Whimsical Naming**: Because even in the apocalypse, a little charm helps.

## Installation

To install `nightly-data-debris-duster`, you'll need [Rust and Cargo](https://www.rust-lang.org/tools/install) installed on your system.

1.  Clone the `ApocalypsAI` repository (if you haven't already):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```
2.  Navigate to the utility's directory:
    ```bash
    cd rust-utils/nightly-data-debris-duster
    ```
3.  Build the project:
    ```bash
    cargo build --release
    ```
4.  The executable will be located at `target/release/nightly-data-debris-duster`.
    For easier access, you can install it to your Cargo bin directory:
    ```bash
    cargo install --path .
    ```
    (Ensure `~/.cargo/bin` is in your system's PATH).

## Usage

Run the `nightly-data-debris-duster` command with the `-p` or `--path` argument, specifying the directory you wish to scan.

```bash
nightly-data-debris-duster --path /path/to/your/data/cache
```

### Example:

```bash
# Assuming you have some duplicate files in ~/scavenged_data
nightly-data-debris-duster -p ~/scavenged_data
```

**Example Output:**

```
Scanning '/home/user/scavenged_data' for data debris...

--- Duplicate Debris (Hash: a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890) ---
  - /home/user/scavenged_data/old_logs/log_archive_2077.txt
  - /home/user/scavenged_data/backup/log_archive_2077_copy.txt
  - /home/user/scavenged_data/temp/log_archive_2077.bak

--- Duplicate Debris (Hash: f0e9d8c7b6a54321f0e9d8c7b6a54321f0e9d8c7b6a54321f0e9d8c7b6a54321) ---
  - /home/user/scavenged_data/images/sunset_wasteland.jpg
  - /home/user/scavenged_data/photos/my_pics/sunset_wasteland_copy.jpg

Dusting complete! Consider clearing this debris to reclaim space.
```

If no duplicates are found:

```bash
Scanning '/home/user/pristine_vault' for data debris...

No duplicate data debris found. Your digital wasteland is pristine!
```

## Development

To run tests:

```bash
cargo test
```
