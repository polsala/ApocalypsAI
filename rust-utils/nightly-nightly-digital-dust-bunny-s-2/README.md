# Nightly Digital Dust Bunny Sweeper

"Sweep away the digital dust bunnies before they multiply!"

`nightly-digital-dust-bunny-sweeper` is a whimsical yet powerful command-line utility written in Rust. It helps you identify and manage digital clutter by scanning specified directories for files that are either very old or excessively large. Think of it as a digital broom, tidying up the forgotten corners of your filesystem.

## Features

*   **High Performance**: Built with Rust for speed and efficiency, especially when traversing large file systems.
*   **Configurable Thresholds**: Define what constitutes a "dust bunny" by setting age and size limits.
*   **Recursive Scanning**: Dive deep into subdirectories to uncover hidden clutter.
*   **Clear Reporting**: Get a concise list of identified files, their sizes, and last modification times.

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
./target/release/nightly-digital-dust-bunny-sweeper --help
```

## Usage

Run the utility from your terminal. By default, it scans the current directory for files older than 365 days or larger than 100 MB.

```bash
nightly-digital-dust-bunny-sweeper [OPTIONS]
```

### Options

*   `-p, --path <DIRECTORY>`: The root directory to start scanning from. Defaults to the current directory.
*   `-a, --age <DAYS>`: Files older than this many days will be considered dust bunnies. Defaults to `365`.
*   `-s, --size <MEGABYTES>`: Files larger than this many megabytes will be considered dust bunnies. Defaults to `100`.
*   `-v, --verbose`: Show more detailed output during scanning.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

### Examples

Scan your home directory for files older than 2 years (730 days) or larger than 500 MB:

```bash
nightly-digital-dust-bunny-sweeper --path ~/ --age 730 --size 500
```

Find all files in `/var/log` that are older than 30 days:

```bash
nightly-digital-dust-bunny-sweeper --path /var/log --age 30 --size 0 # size 0 means no size limit
```

Identify large files (over 1GB) anywhere in your `/data` partition, regardless of age:

```bash
nightly-digital-dust-bunny-sweeper --path /data --age 0 --size 1024 # age 0 means no age limit
```

## Contributing

Feel free to contribute to sweeping away more digital dust bunnies! Open issues for bugs or feature requests, or submit pull requests with improvements.
