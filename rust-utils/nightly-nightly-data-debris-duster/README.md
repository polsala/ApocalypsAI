# Nightly Data Debris Duster

A high-performance CLI tool crafted in Rust to help the community identify and report duplicate files within specified directories. In the post-apocalyptic digital landscape, every byte counts, and this tool ensures your scavenged data caches are free of redundant "debris."

## Features

*   **Fast Scanning**: Leverages Rust's performance for quick directory traversal and hashing.
*   **SHA256 Hashing**: Uses robust SHA256 hashes to reliably identify identical file content.
*   **Recursive Scan**: Scans all subdirectories from the specified root path.
*   **Clear Reporting**: Presents duplicate file groups in an easy-to-read format.

## Installation

To use the Nightly Data Debris Duster, you'll need Rust and Cargo installed. If you don't have them, you can install them via `rustup`: [https://rustup.rs/](https://rustup.rs/)

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-data-debris-duster
    ```
2.  **Build the utility:**
    ```bash
    cargo build --release
    ```
3.  **The executable will be located at `target/release/nightly-data-debris-duster`. You can also install it to your Cargo bin directory:**
    ```bash
    cargo install --path .
    ```
    This will make `nightly-data-debris-duster` available in your shell's PATH.

## Usage

Run the `nightly-data-debris-duster` command, providing the path to the directory you wish to scan.

```bash
nightly-data-debris-duster --path /path/to/your/data/cache
```

### Example

```bash
# Assuming you have some duplicate files in ~/my_scavenged_data
nightly-data-debris-duster --path ~/my_scavenged_data
```

**Output Example:**

```
Scanning for digital debris in "/home/user/my_scavenged_data"...

--- Duplicate Debris (Hash: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2) ---
  - /home/user/my_scavenged_data/reports/log_archive_2023.zip
  - /home/user/my_scavenged_data/backups/old_logs/log_archive_2023.zip
  - /home/user/my_scavenged_data/temp/log_archive_copy.zip

--- Duplicate Debris (Hash: f0e1d2c3b4a5f6e7d8c9b0a1f2e3d4c5b6a7f8e9d0c1b2a3f4e5d6c7b8a9f0e1) ---
  - /home/user/my_scavenged_data/documents/manifest_v1.txt
  - /home/user/my_scavenged_data/documents/manifest_final.txt

Digital debris report complete. Time to clear the clutter!
```

If no duplicates are found:

```
Scanning for digital debris in "/home/user/my_scavenged_data"...

No significant digital debris (duplicates) found. Your data is sparkling clean!
```

## Development

To run tests:

```bash
cargo test
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
