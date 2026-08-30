# Nightly Data Rot Purger

## Whimsical Utility: Digital Debris Scavenger

In the post-apocalyptic digital wasteland, data accumulates like radioactive dust. The `nightly-data-rot-purger` is your trusty Rust-powered scavenger, designed to unearth and prioritize 'data rot' – files that are old, large, and likely forgotten. By identifying these digital detritus, you can reclaim precious storage and maintain the vitality of your salvaged systems.

## Features

*   **Efficient Scanning**: Recursively scans directories for files.
*   **Rot Score Calculation**: Assigns a 'rot score' based on a file's age and size, prioritizing the most egregious digital decay.
*   **Configurable Thresholds**: Set minimum age and size to define what constitutes 'rot'.
*   **Top Results Limiting**: Focus on the most critical files with a configurable output limit.
*   **Blazing Fast**: Written in Rust for maximum performance and minimal resource consumption.

## Installation

To use the `nightly-data-rot-purger`, you'll need Rust and Cargo installed. If you don't have them, visit [rustup.rs](https://rustup.rs/).

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-data-rot-purger
    ```
2.  **Build the utility:**
    ```bash
    cargo build --release
    ```
3.  **The executable will be located at `target/release/nightly-data-rot-purger`.**

## Usage

Run the utility from the command line. You can specify the target path, minimum age, minimum size, and the number of results to display.

```bash
./target/release/nightly-data-rot-purger [OPTIONS]
```

### Arguments:

*   `-p, --path <DIRECTORY>`: Path to the directory to scavenge for data rot. Defaults to the current directory (`.`).
*   `-a, --min-age-days <DAYS>`: Minimum age in days for a file to be considered 'rot'. Defaults to `365` (1 year).
*   `-s, --min-size-mb <MB>`: Minimum size in megabytes for a file to be considered 'rot'. Defaults to `10` MB.
*   `-l, --limit <N>`: Limit the number of top 'rot' files to display. Defaults to `10`.

### Examples:

1.  **Scan the current directory with default settings:**
    ```bash
    ./target/release/nightly-data-rot-purger
    ```

2.  **Scan a specific directory (`/var/log`) for files older than 90 days and larger than 50MB, showing top 5:**
    ```bash
    ./target/release/nightly-data-rot-purger -p /var/log -a 90 -s 50 -l 5
    ```

3.  **Find any file older than 5 years (1825 days) regardless of size (by setting min-size-mb to 0):**
    ```bash
    ./target/release/nightly-data-rot-purger -a 1825 -s 0
    ```

## How 'Rot Score' is Calculated

The 'rot score' is a simple metric: `(file_age_in_days) * (file_size_in_megabytes)`. This prioritizes files that are both very old and very large, as they are often the most impactful to system health when left unmanaged.

## Contributing

Feel free to contribute to the `nightly-data-rot-purger` by submitting issues or pull requests. Let's keep the digital wasteland tidy!
