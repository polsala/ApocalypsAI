# Nightly Digital Dust Bunny Collector

A high-performance CLI tool written in Rust to find and manage old, forgotten files (affectionately dubbed 'digital dust bunnies') in your filesystem. Keep your digital space tidy and reclaim lost storage!

## Features

*   **Fast Scanning**: Leverages Rust's performance for quick directory traversal.
*   **Age-Based Filtering**: Identify files older than a specified number of days.
*   **List or Move**: Either list the found dust bunnies or automatically move them to a designated 'digital landfill' directory.
*   **Recursive Scan**: Scans subdirectories to catch all hidden dust bunnies.

## Installation

To install `nightly-dust-bunny-collector`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/) for instructions.

1.  **Clone the repository (or download the utility folder):**
    ```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-dust-bunny-collector
    ```

2.  **Build and install using Cargo:**
    ```bash
cargo install --path .
    ```
    This will install the `nightly-dust-bunny-collector` executable to your Cargo bin directory (usually `~/.cargo/bin`). Make sure this directory is in your system's PATH.

### Dependencies

The `Cargo.toml` for this utility uses the following dependencies:

```toml
[package]
name = "nightly-dust-bunny-collector"
version = "0.1.0"
edition = "2021"

[dependencies]
clap = { version = "4.0", features = ["derive"] }
walkdir = "2.3"
chrono = "0.4"

[dev-dependencies]
tempfile = "3.0"
assert_cmd = "2.0"
predicates = "0.1"
filetime = "0.2" # For setting file modification times in tests
```

## Usage

```bash
nightly-dust-bunny-collector --help
```

### Examples:

1.  **List all files in your home directory older than 1 year (365 days):**
    ```bash
nightly-dust-bunny-collector --path ~/ --age 365 list
    ```

2.  **Move all files in your `~/Downloads` directory older than 90 days to a `~/DigitalLandfill` folder:**
    ```bash
mkdir -p ~/DigitalLandfill # Ensure the destination exists
nightly-dust-bunny-collector --path ~/Downloads --age 90 move --destination ~/DigitalLandfill
    ```

3.  **List files in a specific project folder older than 2 years:**
    ```bash
nightly-dust-bunny-collector --path /path/to/my/old_project --age 730 list
    ```

## Development & Testing

To run the tests:

```bash
cargo test
```

The tests create temporary directories and files to simulate different scenarios, ensuring the utility works as expected without touching your actual files.
