# Nightly Digital Dust Bunny Sweeper

`nightly-digital-dust-bunny` is a whimsical yet practical command-line utility designed to help you identify and report on old, potentially unused files lurking in your file system. Think of them as 'digital dust bunnies' – files that have accumulated over time, taking up space and contributing to digital clutter.

This tool scans specified directories, identifies files older than a given threshold, and calculates a 'fluffiness' score based on their age and size. It's a great way to get an overview of your digital hygiene without actually deleting anything.

## Features

*   **High Performance**: Built with Rust for fast and efficient file system traversal.
*   **Configurable Age Threshold**: Specify how old a file needs to be to be considered a 'dust bunny'.
*   **'Fluffiness' Score**: A fun metric combining file age and size to indicate how much 'clutter' a file represents.
*   **Non-Destructive**: Only reports, never deletes or modifies your files.
*   **Recursive Scanning**: Dives deep into subdirectories to find hidden bunnies.

## Installation

To install `nightly-digital-dust-bunny`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/) for instructions.

Once Rust is set up, you can install the utility directly from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-digital-dust-bunny
cargo install --path .
```

This will compile the tool and place the `dust-bunny` executable in your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage

Run `dust-bunny` with the path you want to scan and an optional age threshold in days.

```bash
dust-bunny [OPTIONS] <PATH>
```

### Arguments

*   `<PATH>`: The directory to scan for digital dust bunnies.

### Options

*   `-a, --age <DAYS>`: The minimum age in days for a file to be considered a 'dust bunny'. Files older than this will be reported. Defaults to `90` days.
*   `-v, --verbose`: Enable verbose output, showing more details about each file.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

## Examples

1.  **Scan your current directory for files older than 90 days (default):**

    ```bash
dust-bunny .
    ```

2.  **Scan your home directory for files older than 180 days:**

    ```bash
dust-bunny ~/documents --age 180
    ```

3.  **Scan a specific project directory with verbose output:**

    ```bash
dust-bunny /var/log --age 30 -v
    ```

## Output Format

The tool will output a list of identified digital dust bunnies, including:

*   **Path**: The full path to the file.
*   **Size**: The size of the file (e.g., 1.2 MB).
*   **Age**: How old the file is (e.g., 125 days).
*   **Fluffiness Score**: A calculated score (age_in_days * size_in_kb / 1000) indicating its 'fluffiness'. Higher score means a bigger, older dust bunny!

Example output:

```
Digital Dust Bunnies found in './temp':
---------------------------------------
Path: ./temp/old_report.pdf, Size: 2.5 MB, Age: 150 days, Fluffiness: 375.0
Path: ./temp/archive/unused_data.zip, Size: 10.1 MB, Age: 200 days, Fluffiness: 2020.0
Path: ./temp/logs/debug.log, Size: 0.8 MB, Age: 100 days, Fluffiness: 80.0
---------------------------------------
Total Dust Bunnies: 3
```
