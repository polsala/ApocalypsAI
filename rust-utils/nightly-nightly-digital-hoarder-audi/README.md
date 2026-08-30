# nightly-digital-hoarder-audit

A high-performance CLI tool for the ApocalypsAI community to audit disk usage by file type and size, helping identify digital hoarding patterns in the post-collapse data-scape. Unearth the forgotten digital treasures and trash of the pre-collapse era!

## Features

-   Recursively scans a specified directory.
-   Aggregates file counts and total sizes by file extension.
-   Identifies top N largest files and directories.
-   Provides a summary report of disk usage.

## Installation

Ensure you have Rust and Cargo installed.

```bash
# Clone the repository (or navigate to the utility's directory)
# git clone https://github.com/polsala/ApocalypsAI.git
# cd ApocalypsAI/rust-utils/nightly-digital-hoarder-audit

# Build the utility
cargo build --release

# The executable will be in target/release/
# You might want to add it to your PATH or move it to a bin directory.
```

## Usage

```bash
./target/release/nightly-digital-hoarder-audit <PATH> [OPTIONS]
```

### Arguments

-   `<PATH>`: The root directory to start the audit from.

### Options

-   `-n, --top-n <TOP_N>`: Number of top largest files/directories to display (default: 5).
-   `-m, --min-size <MIN_SIZE>`: Minimum file size (e.g., "10MB", "1GB") to include in the detailed file list.
-   `-e, --extensions <EXTENSIONS>`: Comma-separated list of extensions to include (e.g., "jpg,png,mp4"). If not specified, all extensions are included.
-   `-v, --verbose`: Show more detailed output, including individual files.
-   `-h, --help`: Print help information.

### Examples

```bash
# Audit the current directory
./target/release/nightly-digital-hoarder-audit .

# Audit a specific directory, showing top 10 items
./target/release/nightly-digital-hoarder-audit /var/log -n 10

# Audit only image files larger than 1MB
./target/release/nightly-digital-hoarder-audit ~/Pictures -e jpg,png -m 1MB

# Verbose audit of a project directory
./target/release/nightly-digital-hoarder-audit ~/my_project -v
```
