## nightly-rust-file-sync

A whimsical yet useful standalone utility for synchronizing files between two directories using Rust. It offers high performance and optional checksum verification to ensure data integrity.

### Philosophy

*   **Speed and Reliability**: Built with Rust for maximum performance and safety.
*   **Simplicity**: Easy to use CLI interface.
*   **Integrity**: Optional checksum verification to prevent data corruption.

### Installation

To build and install this utility, you'll need Rust and Cargo installed.

1.  Clone the repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```

2.  Navigate to the utility's directory:
    ```bash
    cd rust-utils/nightly-rust-file-sync
    ```

3.  Build the project:
    ```bash
    cargo build --release
    ```

4.  The executable will be in `target/release/nightly-rust-file-sync`. You can copy it to your PATH or run it directly.

### Usage

```bash
nightly-rust-file-sync <source_dir> <destination_dir> [--verify-checksum]
```

*   `<source_dir>`: The directory to copy files from.
*   `<destination_dir>`: The directory to copy files to.
*   `--verify-checksum`: (Optional) If provided, the tool will calculate and compare SHA256 checksums of files before copying. This adds overhead but ensures data integrity.

### Examples

Synchronize `~/wasteland_supplies` to `/mnt/apocalypse_bunker`:

```bash
nightly-rust-file-sync ~/wasteland_supplies /mnt/apocalypse_bunker
```

Synchronize and verify checksums:

```bash
nightly-rust-file-sync ~/wasteland_supplies /mnt/apocalypse_bunker --verify-checksum
```

### Testing

To run the included tests:

```bash
cd rust-utils/nightly-rust-file-sync
cargo test
```

### Contributing

Contributions are welcome! Please follow the ApocalypsAI contribution guidelines.
