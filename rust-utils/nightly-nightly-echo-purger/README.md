# nightly-echo-purger

A high-performance Rust CLI tool to detect and report duplicate files, purging "data echoes" from your digital wasteland.

## Summary

In the post-apocalyptic digital age, data echoes can accumulate, consuming precious storage and causing confusion. The `nightly-echo-purger` is your trusty companion for identifying and eliminating these redundant files. It uses blazing-fast SHA256 hashing to find exact duplicates across specified directories, offering a dry-run mode for safety and a purge mode for decisive action.

## Features

*   **High Performance:** Written in Rust for speed and efficiency in file system traversal and hashing.
*   **SHA256 Hashing:** Ensures accurate content-based duplicate detection.
*   **Multiple Directory Support:** Scan one or more paths for echoes.
*   **Dry Run Mode:** Preview duplicates without making any changes.
*   **Purge Mode:** Safely delete duplicate files (keeping one original).
*   **Whimsical Output:** Reports findings with a touch of apocalyptic charm.

## Installation

1.  **Prerequisites:** Ensure you have Rust and Cargo installed. If not, follow the instructions at [rust-lang.org](https://www.rust-lang.org/tools/install).
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-echo-purger
    ```
3.  **Build the utility:**
    ```bash
    cargo build --release
    ```
4.  **Run from target:**
    ```bash
    ./target/release/nightly-echo-purger --help
    ```
5.  **Add to PATH (optional):** For easier access, you might want to add `~/.cargo/bin` or the `target/release` directory to your system's PATH.

## Usage

```bash
nightly-echo-purger [OPTIONS] <PATHS>...
```

### Arguments

*   `<PATHS>...`: One or more paths to directories to scan for duplicate files.

### Options

*   `-d, --delete`: **DANGER!** Delete duplicate files, keeping only the first encountered instance. Use with caution.
*   `-v, --verbose`: Enable verbose output, showing more details during scanning.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

### Examples

1.  **Dry run to find echoes in current directory and a 'scavenged' folder:**
    ```bash
    nightly-echo-purger . ./scavenged_data
    ```

2.  **Verbose dry run across multiple wasteland sectors:**
    ```bash
    nightly-echo-purger -v /var/log/wasteland /home/survivor/cache /mnt/old_archives
    ```

3.  **Purge echoes from your temporary cache (use with extreme caution!):**
    ```bash
    nightly-echo-purger --delete ./temp_cache
    ```

## Tests

To run the tests, navigate to the utility's directory and use Cargo:

```bash
cargo test
```
