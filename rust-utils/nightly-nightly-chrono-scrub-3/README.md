# Nightly Chrono-Scrub: Digital Temporal Decay Scrubber

`nightly-chrono-scrub` is a high-performance Rust CLI tool designed to help you manage digital entropy by identifying and optionally removing files that have succumbed to temporal decay (i.e., are older than a specified duration).

It's like a digital archaeologist, sifting through the sands of time to reclaim valuable storage space and keep your file systems pristine.

## Features

*   **Blazing Fast**: Written in Rust for maximum performance when traversing large directories.
*   **Configurable Decay**: Specify how old files need to be (e.g., `30d`, `1w`, `2y`).
*   **Dry Run Mode**: Safely preview which files would be affected before making any changes.
*   **Interactive Deletion**: Confirm each deletion or force removal.
*   **Exclusion Patterns**: Ignore files or directories matching specified patterns.
*   **Whimsical Output**: Enjoy themed messages about digital entropy and temporal echoes.

## Installation

To install `nightly-chrono-scrub`, ensure you have Rust and Cargo installed. Then, run:

```bash
cargo install --path .
```

Or, if you clone the repository:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-chrono-scrub
cargo install --path .
```

This will compile the utility and place the `chrono-scrub` executable in your Cargo bin directory (usually `~/.cargo/bin`).

## Usage

```bash
chrono-scrub --help
```

```
A high-performance Rust CLI tool to identify and optionally remove files older than a specified duration.

Usage: chrono-scrub [OPTIONS] <PATH>

Arguments:
  <PATH>  The directory to scan for decayed files

Options:
  -d, --duration <DURATION>  Files older than this duration will be considered for scrubbing (e.g., "30d", "1w", "2y") [default: 30d]
  -x, --exclude <EXCLUDE>    Exclude files or directories matching this glob pattern (can be specified multiple times)
  -n, --dry-run              Only list files that would be scrubbed, do not delete them
  -f, --force                Skip interactive confirmation when deleting files
  -v, --verbose              Enable verbose output
  -h, --help                 Print help
  -V, --version              Print version
```

### Examples

1.  **Dry run: See files older than 60 days in the current directory**

    ```bash
    chrono-scrub . --duration 60d --dry-run
    ```

    _Output will list files that would be removed, without actually deleting them._

2.  **Scrub files older than 1 year in `/var/log` (with confirmation)**

    ```bash
    chrono-scrub /var/log --duration 1y
    ```

    _For each file, it will prompt `Delete 'file.log'? (y/N):`_

3.  **Force scrub files older than 7 days in `~/downloads`, excluding `.torrent` files**

    ```bash
    chrono-scrub ~/downloads --duration 7d --force --exclude "*.torrent"
    ```

    _This will delete all matching files without asking for confirmation._

4.  **Scrub files older than 3 months in a specific project directory, excluding `node_modules`**

    ```bash
    chrono-scrub ./my_project --duration 3M --exclude "node_modules/**" --exclude "target/**"
    ```

## Duration Format

The `--duration` argument accepts a number followed by a unit:

*   `d`: days (e.g., `30d`)
*   `w`: weeks (e.g., `2w`)
*   `M`: months (e.g., `6M`)
*   `y`: years (e.g., `1y`)

If no unit is specified, days are assumed (e.g., `90` is `90d`).

## Contributing

Feel free to contribute to the `nightly-chrono-scrub` project! Report issues, suggest features, or submit pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
