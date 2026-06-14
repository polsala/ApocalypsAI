# Nightly Temporal Dust Sweeper

The digital realm, much like the physical, accumulates its own form of dust: files long forgotten, untouched by human or machine for eons (or at least, a few months). The `nightly-temporal-dust-sweeper` is your trusty broom, a high-performance Rust CLI tool designed to meticulously scan your directories for these "temporal dust bunnies" – files that haven't been accessed or modified within a specified timeframe.

It won't delete anything (we're not *that* apocalyptic), but it will provide a clear report, allowing you to decide which digital relics to archive, relocate, or finally bid farewell to.

## Features

*   **Blazing Fast**: Written in Rust for maximum performance, especially on large file systems.
*   **Configurable Threshold**: Define what constitutes a "dust bunny" by setting a duration (e.g., 90 days, 1 year).
*   **Detailed Reporting**: Lists file paths, their last access/modification time, and how long ago that was.
*   **Safe**: Only reports, never modifies or deletes files.

## Installation

1.  **Prerequisites**: Ensure you have Rust and Cargo installed. If not, visit [rustup.rs](https://rustup.rs/).
2.  **Build from source**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-temporal-dust-sweeper
    cargo build --release
    ```
3.  **Run**: The executable will be found at `target/release/nightly-temporal-dust-sweeper`. You might want to add it to your system's PATH.

## Usage

```bash
nightly-temporal-dust-sweeper [OPTIONS] <PATH>
```

### Arguments

*   `<PATH>`: The directory to scan for temporal dust bunnies.

### Options

*   `-d, --days <DAYS>`: The minimum number of days a file must be untouched to be considered a dust bunny. Defaults to 90 days.
*   `-m, --modified`: Use last modification time instead of last access time. (Note: Access time tracking can be disabled on some filesystems for performance, making `--modified` a more reliable option in those cases.)
*   `-v, --verbose`: Show more detailed output, including the exact timestamp.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

## Examples

1.  **Scan your home directory for files untouched in the last 180 days (using access time):**
    ```bash
    nightly-temporal-dust-sweeper ~/ --days 180
    ```

2.  **Scan a project directory for files not modified in the last year (365 days):**
    ```bash
    nightly-temporal-dust-sweeper /path/to/my/project --days 365 --modified
    ```

3.  **Verbose output for files untouched in the last 30 days in the current directory:**
    ```bash
    nightly-temporal-dust-sweeper . --days 30 -v
    ```

## Contributing

Feel free to open issues or submit pull requests!
