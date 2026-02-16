# Nightly Digital Dust Bunny Sweeper

## Overview

The `nightly-dust-bunny-sweeper` is a whimsical yet practical command-line utility written in Rust. It helps you identify and manage 'digital dust bunnies' – those old, forgotten files lurking in your filesystem, consuming precious storage space and mental bandwidth. Think of it as a high-performance digital broom for your directories!

It scans a specified directory for files older than a given duration and can optionally move them to a designated 'digital compost bin' (an archive directory) for later review or permanent deletion.

## Features

*   **Blazing Fast**: Built with Rust for optimal performance when traversing large filesystems.
*   **Configurable Age**: Specify how old a file must be to be considered a 'dust bunny'.
*   **Compost Bin**: Safely move identified files to an archive directory instead of immediately deleting them.
*   **Whimsical Reporting**: Get a summary of your digital clutter with a touch of apocalyptic charm.

## Installation

To install `nightly-dust-bunny-sweeper`, you'll need Rust and Cargo installed on your system. If you don't have them, visit [rustup.rs](https://rustup.rs/) for installation instructions.

```bash
cargo install nightly-dust-bunny-sweeper
```

Alternatively, you can clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-dust-bunny-sweeper
cargo build --release
# The executable will be found at target/release/nightly-dust-bunny-sweeper
```

## Usage

```bash
nightly-dust-bunny-sweeper --help
```

```
A high-performance CLI tool to find and 'compost' old, unused files.

Usage: nightly-dust-bunny-sweeper [OPTIONS] <PATH>

Arguments:
  <PATH>  The directory to scan for digital dust bunnies

Options:
  -a, --age-days <AGE_DAYS>          Files older than this many days will be considered dust bunnies [default: 365]
  -c, --compost-dir <COMPOST_DIR>    Optional directory to move identified dust bunnies to. If not provided, files are only listed.
  -f, --force                        Perform composting without confirmation (use with caution!)
  -h, --help                         Print help
  -V, --version                      Print version
```

### Examples

1.  **List all files older than 90 days in your downloads directory:**

    ```bash
    nightly-dust-bunny-sweeper ~/Downloads --age-days 90
    ```

2.  **Move files older than 180 days from your documents to a 'compost' folder:**

    ```bash
    mkdir -p ~/DigitalCompost
    nightly-dust-bunny-sweeper ~/Documents --age-days 180 --compost-dir ~/DigitalCompost
    ```

    The tool will prompt for confirmation before moving files unless `--force` is used.

3.  **Force-compost files older than 2 years in a project directory:**

    ```bash
    nightly-dust-bunny-sweeper ~/Projects/OldProject --age-days 730 --compost-dir ~/DigitalCompost --force
    ```

## Contributing

Contributions are welcome! Feel free to open issues or pull requests on the main ApocalypsAI repository.
