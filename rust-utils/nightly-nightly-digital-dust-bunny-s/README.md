# nightly-digital-dust-bunny-sweeper

A high-performance Rust CLI tool designed to help you identify and report on "digital dust bunnies" – stale or unused files and directories that accumulate over time, cluttering your system. This tool scans specified paths and reports on items older than a given age or larger than a certain size, without deleting anything. It's your friendly digital janitor, providing insights to keep your digital space tidy.

## Features

- **Fast Scanning**: Leverages Rust's performance for quick file system traversal.
- **Age-based Detection**: Identify files/directories not modified for a specified duration.
- **Size-based Detection**: Pinpoint large files/directories consuming significant space.
- **Customizable Thresholds**: Define what constitutes a "dust bunny" with flexible arguments.
- **Safe Reporting**: Only reports; never deletes or modifies files.
- **Whimsical Output**: Categorizes findings with a touch of charm.

## Installation

To install `nightly-digital-dust-bunny-sweeper`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/) for instructions.

```bash
cargo install nightly-digital-dust-bunny-sweeper
```

Alternatively, clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-digital-dust-bunny-sweeper
cargo build --release
# The executable will be found at target/release/nightly-digital-dust-bunny-sweeper
```

## Usage

Run the `dust-bunny-sweeper` command with the desired path and criteria.

```bash
dust-bunny-sweeper [OPTIONS] <PATH>
```

### Arguments

- `<PATH>`: The root directory to start scanning from.

### Options

- `-a, --age <DAYS>`: Report files/directories not modified in the last `DAYS` days. (e.g., `--age 90` for 90 days).
- `-s, --size <MB>`: Report files/directories larger than `MB` megabytes. (e.g., `--size 100` for 100 MB).
- `-v, --verbose`: Show more detailed information about each dust bunny.
- `-h, --help`: Print help information.
- `-V, --version`: Print version information.

### Examples

Scan your current directory for files/folders older than 180 days:

```bash
dust-bunny-sweeper . --age 180
```

Scan your home directory for files/folders larger than 500 MB:

```bash
dust-bunny-sweeper ~/ --size 500
```

Scan a specific project directory for anything older than 30 days or larger than 10 MB, with verbose output:

```bash
dust-bunny-sweeper /path/to/my/project --age 30 --size 10 --verbose
```

## Development

To run tests:

```bash
cargo test
```

## License

This project is licensed under the MIT License.
