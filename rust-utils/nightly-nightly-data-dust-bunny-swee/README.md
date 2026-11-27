# Nightly Data Dust Bunny Sweeper

A high-performance Rust CLI tool designed to help you identify and report on old, unaccessed files – your 'data dust bunnies' – lurking in your digital archives. Keep your systems tidy and reclaim precious storage space by understanding where your forgotten data resides.

## Features

*   **Recursive Scanning**: Traverses directories to find all files.
*   **Age Categorization**: Classifies files into 'Fresh', 'Stale', 'Ancient', and 'Fossilized' based on their last access time.
*   **Performance**: Built with Rust for speed and efficiency, ideal for large file systems.
*   **Verbose Output**: Option to see details for each file found.
*   **Summary Report**: Provides a concise overview of files in each category.

## Installation

To install the `nightly-data-dust-bunny-sweeper` CLI tool, you need to have Rust and Cargo installed. If you don't, visit [rust-lang.org](https://www.rust-lang.org/tools/install).

1.  **Clone the repository (or navigate to the utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-data-dust-bunny-sweeper
    ```
2.  **Build and install:**
    ```bash
    cargo install --path .
    ```
    This will install the `nightly-data-dust-bunny-sweeper` executable to your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage

Run the `nightly-data-dust-bunny-sweeper` command followed by the path to the directory you want to scan.

```bash
nightly-data-dust-bunny-sweeper <PATH_TO_DIRECTORY> [OPTIONS]
```

### Arguments

*   `<PATH_TO_DIRECTORY>`: The path to the directory you want to sweep for data dust bunnies.

### Options

*   `-v`, `--verbose`: Show verbose output, listing each file found and its category.
*   `-h`, `--help`: Print help information.
*   `-V`, `--version`: Print version information.

### Examples

1.  **Scan your home directory for a summary report:**
    ```bash
    nightly-data-dust-bunny-sweeper ~/Documents
    ```

2.  **Scan a specific project directory with verbose output:**
    ```bash
    nightly-data-dust-bunny-sweeper /var/log --verbose
    ```

## File Categories

*   **Fresh**: Files accessed less than 30 days ago.
*   **Stale**: Files accessed between 30 and 90 days ago.
*   **Ancient**: Files accessed between 90 days and 1 year ago.
*   **Fossilized**: Files accessed more than 1 year ago.
*   **Unknown**: Files for which access metadata could not be retrieved.
