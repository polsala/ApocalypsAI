# Nightly Digital Relic Hunter

## Unearthing the Past: Your Digital Archaeology Assistant

The `nightly-digital-relic-hunter` is a blazing-fast Rust CLI tool designed to help you discover and categorize files that have been untouched for an extended period. Think of it as your personal digital archaeologist, sifting through the sands of time (your filesystem) to unearth forgotten data, old logs, or long-abandoned projects. Identify these 'digital relics' to better understand your storage usage, perform cleanups, or simply marvel at the history of your digital domain.

### Features

*   **High Performance**: Written in Rust for speed and efficiency, ideal for large filesystems.
*   **Recursive Scanning**: Traverses directories to find relics deep within your file structure.
*   **Configurable Age**: Specify the minimum age (in days) for a file to be considered a relic.
*   **Detailed Output**: Provides file path, last modification date, size, and calculated age.

### Installation

To use the Digital Relic Hunter, you'll need Rust and Cargo installed. If you don't have them, visit [rustup.rs](https://rustup.rs/) for installation instructions.

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-digital-relic-hunter
    ```
2.  **Build the utility:**
    ```bash
    cargo build --release
    ```
3.  **The executable will be located at `target/release/nightly-digital-relic-hunter`.**

### Usage

Run the utility from the command line, specifying the path to scan and optionally the minimum age in days.

```bash
./target/release/nightly-digital-relic-hunter -p <PATH_TO_SCAN> [-d <MIN_AGE_DAYS>]
```

**Arguments:**

*   `-p`, `--path <PATH>`: **Required**. The directory path to start scanning for relics.
*   `-d`, `--min-age-days <DAYS>`: **Optional**. The minimum age in days for a file to be considered a relic. Defaults to `90` days.

### Examples

1.  **Scan your home directory for files older than 90 days (default):**
    ```bash
    ./target/release/nightly-digital-relic-hunter -p ~/Documents
    ```

2.  **Scan a specific project directory for files older than 365 days (1 year):**
    ```bash
    ./target/release/nightly-digital-relic-hunter -p /var/log -d 365
    ```

3.  **If no relics are found:**
    ```
    No digital relics found older than 90 days in '/home/user/Documents'. Your digital space is pristine!
    ```

4.  **Example output when relics are found:**
    ```
    Discovered 2 digital relics older than 90 days in '/home/user/Documents':
    PATH                                                                   LAST MODIFIED (UTC)       SIZE (bytes)    AGE (days)
    ------------------------------------------------------------------------------------------------------------------------
    /home/user/Documents/old_project/legacy_report.pdf                     2023-01-15 14:30:00       123456          285
    /home/user/Documents/archive/forgotten_notes.txt                       2022-11-01 09:00:00       789             350
    ```

### Development

To run tests:

```bash
cargo test
```

To check code style and potential issues:

```bash
cargo clippy
```
