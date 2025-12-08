# Nightly Temporal Dust Bunny Sweeper

## Overview
`nightly-temporal-dust-bunny-sweeper` is a whimsical yet practical command-line utility written in Rust. It helps you identify "temporal dust bunnies" – files that haven't been accessed or modified for a specified period. Think of it as a digital broom for your file system, helping you find forgotten clutter.

This tool is designed for performance, making it suitable for scanning large directories efficiently.

## Features
*   **High Performance**: Built with Rust for speed and efficiency.
*   **Recursive Scanning**: Traverses directories to find old files everywhere.
*   **Configurable Age**: Specify how many days old a file must be to be considered a "dust bunny."
*   **Clear Reporting**: Lists all identified temporal dust bunnies.

## Installation
To install `nightly-temporal-dust-bunny-sweeper`, you need to have Rust and Cargo installed. If you don't, visit [rust-lang.org](https://www.rust-lang.org/tools/install).

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-temporal-dust-bunny-sweeper
    ```
2.  **Build and install:**
    ```bash
    cargo install --path .
    ```
    This will install the `nightly-temporal-dust-bunny-sweeper` executable to your Cargo bin directory (usually `~/.cargo/bin`). Make sure this directory is in your system's PATH.

## Usage
Run the `nightly-temporal-dust-bunny-sweeper` command with the desired path and age.

```bash
nightly-temporal-dust-bunny-sweeper [OPTIONS]
```

### Arguments
*   `-p`, `--path <PATH>`: The root directory to start sweeping from. Defaults to the current directory (`.`).
*   `-a`, `--age-days <DAYS>`: The age in days after which a file is considered a 'dust bunny' (not accessed or modified). Defaults to `90` days.

### Examples

1.  **Scan the current directory for files older than 90 days (default):**
    ```bash
    nightly-temporal-dust-bunny-sweeper
    ```

2.  **Scan a specific directory (`/var/log/old_archives`) for files older than 365 days:**
    ```bash
    nightly-temporal-dust-bunny-sweeper -p /var/log/old_archives -a 365
    ```

3.  **Scan your home directory for files older than 30 days:**
    ```bash
    nightly-temporal-dust-bunny-sweeper --path ~/ --age-days 30
    ```

## How it Works
The tool recursively walks through the specified directory. For each file, it retrieves its last modification time and last access time. If *both* of these timestamps are older than the calculated cutoff time (current time minus `age_days`), the file is identified and printed as a "temporal dust bunny."

**Note on Access Times**: On some file systems or configurations (e.g., `noatime` mount option), access times might not be accurately updated. In such cases, the tool will primarily rely on modification times, and if access time is unavailable, it will assume it's old for the purpose of the check.
