# Nightly Cosmic Dust Collector

A high-performance CLI tool written in Rust that scans specified directories for small, forgotten "cosmic dust" files and offers to delete them, helping to keep your digital space tidy.

## ✨ Features

-   **Recursive Scanning**: Traverses directories to find dust files everywhere.
-   **Configurable Size Threshold**: Define what constitutes "cosmic dust" (e.g., files smaller than 1KB, 10MB).
-   **Dry Run Mode**: Preview which files would be affected without making any changes.
-   **Safe Deletion**: Requires explicit confirmation before deleting files.
-   **Performance**: Built with Rust for speed and efficiency in file system operations.

## 🚀 Installation

### Prerequisites

-   Rust toolchain (Rustup recommended): `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

### From Source

1.  Clone the repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-cosmic-dust-collector
    ```
2.  Build the project:
    ```bash
    cargo build --release
    ```
3.  The executable will be located at `target/release/nightly-cosmic-dust-collector`. You can move it to your `$PATH` for easier access:
    ```bash
    sudo mv target/release/nightly-cosmic-dust-collector /usr/local/bin/
    ```

## 💡 Usage

```bash
nightly-cosmic-dust-collector [OPTIONS]
```

### Arguments

-   `-p, --path <PATH>`: Directory to scan for cosmic dust. Defaults to the current directory (`.`).
-   `-m, --max-size <SIZE>`: Maximum file size to consider as 'cosmic dust' (e.g., `1KB`, `500B`, `10MB`). Defaults to `1KB`.
-   `-d, --dry-run`: Perform a dry run without deleting any files.
-   `-D, --delete`: Delete the identified cosmic dust files (requires confirmation).

### Examples

1.  **Scan current directory for files smaller than 500 bytes (dry run):**
    ```bash
    nightly-cosmic-dust-collector --max-size 500B --dry-run
    ```

2.  **Scan a specific directory (`~/Downloads`) for files smaller than 10KB and report:**
    ```bash
    nightly-cosmic-dust-collector --path ~/Downloads --max-size 10KB
    ```
    (This will report files but not delete them, as `--delete` is not specified.)

3.  **Delete files smaller than 1KB in the current directory (requires confirmation):**
    ```bash
    nightly-cosmic-dust-collector --max-size 1KB --delete
    ```

4.  **Scan a large directory for very small files (e.g., 100 bytes) and delete them:**
    ```bash
    nightly-cosmic-dust-collector -p /var/log -m 100B -D
    ```

## 🧪 Testing

To run the tests, navigate to the utility's directory and execute:

```bash
cargo test
```

The tests create temporary directories and files to ensure deterministic and isolated execution without affecting your actual file system.
