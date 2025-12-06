# Nightly Temporal Dust Sweeper

A high-performance Rust CLI tool designed to help you clean up your digital wasteland by identifying and optionally removing "temporal dust" — old, unused files that accumulate over time.

## ✨ Features

*   **Efficient Scanning**: Utilizes `walkdir` for fast directory traversal.
*   **Age-Based Filtering**: Identify files older than a specified number of days.
*   **Time Reference**: Filter by last modification time (default) or last access time.
*   **Pattern Matching**: Filter files by regular expression patterns in their names.
*   **Extension Filtering**: Target specific file types (e.g., `.log`, `.tmp`).
*   **Dry Run Mode**: Safely preview which files would be swept without deleting anything.
*   **Sweep Mode**: Permanently remove identified files.
*   **Whimsical Output**: Adds a touch of apocalyptic charm to your cleanup routine.

## 📦 Installation

To install the Temporal Dust Sweeper, you'll need Rust and Cargo installed on your system. If you don't have them, visit [rust-lang.org](https://www.rust-lang.org/).

```bash
cargo install nightly-temporal-dust-sweeper
```

Alternatively, you can clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-temporal-dust-sweeper
cargo build --release
# The executable will be in target/release/nightly-temporal-dust-sweeper
```

## 💻 Usage

```bash
nightly-temporal-dust-sweeper [OPTIONS]
```

### Options

*   `-p, --path <PATH>`: Path to the directory to sweep (default: current directory `.`)
*   `-a, --age-days <DAYS>`: Files older than this many days will be considered 'dust' (default: `30`)
*   `-d, --dry-run`: Perform a dry run: list files that would be swept, but don't delete them.
*   `-s, --sweep`: Actually sweep (delete) the identified temporal dust. **Use with caution!**
*   `-A, --access-time`: Use last access time instead of last modification time for age calculation.
*   `-P, --pattern <REGEX>`: Only consider files matching this regex pattern (e.g., `".*\\.log$"`).
*   `-e, --extension <EXT>`: Only consider files with this extension (e.g., `log`, `tmp`).

### Examples

1.  **List all files older than 60 days in the current directory (dry run):**

    ```bash
    nightly-temporal-dust-sweeper --age-days 60 --dry-run
    ```

2.  **Sweep (delete) all `.tmp` files older than 7 days in a specific directory:**

    ```bash
    nightly-temporal-dust-sweeper --path /var/log/old_temps --age-days 7 --extension tmp --sweep
    ```

3.  **Find old log files matching a specific pattern, using access time:**

    ```bash
    nightly-temporal-dust-sweeper --path /var/log --age-days 90 --access-time --pattern "^app_error_.*\.log$" --dry-run
    ```

4.  **List all files older than the default 30 days (dry run is default if no action specified):**

    ```bash
    nightly-temporal-dust-sweeper
    ```

    (This will perform a dry run by default, listing files older than 30 days in the current directory.)

## ⚠️ Warning

Using the `--sweep` flag will permanently delete files. Always perform a `--dry-run` first to ensure you are only targeting the intended files. The ApocalypsAI Nightly Integrator agent is not responsible for any data loss caused by reckless sweeping.
