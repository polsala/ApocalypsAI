# Nightly Stellar Dust Sweeper

A high-performance CLI tool to identify and list "stellar dust" (old, unused files) across your filesystem, helping you declutter with cosmic efficiency. Think of it as a cosmic broom for your digital space, sweeping away files that have been dormant for too long.

## Features

*   **Blazing Fast**: Written in Rust for optimal performance when scanning large directories.
*   **Configurable Age**: Specify how old a file must be to be considered "stellar dust" (e.g., 90 days, 6 months, 1 year).
*   **Recursive Scan**: Traverses directories recursively to find dust bunnies hiding deep within.
*   **Clear Output**: Lists files with their path, size, and last modification date.

## Installation

Make sure you have [Rust and Cargo](https://www.rust-lang.org/tools/install) installed.

```bash
cargo install nightly-stellar-dust-sweeper
```

Or, if you've cloned the repository:

```bash
cargo build --release
# The executable will be in ./target/release/nightly-stellar-dust-sweeper
```

## Usage

```bash
nightly-stellar-dust-sweeper [OPTIONS] <PATH>
```

### Arguments

*   `<PATH>`: The directory to start sweeping for stellar dust.

### Options

*   `-d, --days <DAYS>`: Files older than this many days will be considered dust. (Default: 90 if no other age option is specified)
*   `-m, --months <MONTHS>`: Files older than this many months will be considered dust.
*   `-y, --years <YEARS>`: Files older than this many years will be considered dust.
*   `-s, --sort-by <FIELD>`: Sort results by 'path', 'size', or 'age'. (Default: age)
*   `-r, --reverse`: Reverse the sort order.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

### Examples

1.  **Find all files older than 180 days in the current directory:**
    ```bash
    nightly-stellar-dust-sweeper --days 180 .
    ```

2.  **Find files older than 1 year in your documents folder, sorted by size:**
    ```bash
    nightly-stellar-dust-sweeper --years 1 ~/Documents --sort-by size
    ```

3.  **List all dust in `/var/log` that's older than 3 months, sorted by path in reverse order:**
    ```bash
    nightly-stellar-dust-sweeper --months 3 /var/log --sort-by path --reverse
    ```

## How it Works

The tool uses the file's last modification timestamp to determine its age. It efficiently walks the specified directory, collects metadata for each file, and filters based on your provided age threshold. The results are then presented in a human-readable format, ready for your review and potential cleanup.
