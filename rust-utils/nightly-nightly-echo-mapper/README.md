# Nightly Echo Mapper

## Whimsical Concept

In the ever-shifting sands of the post-apocalyptic digital wasteland, files are not merely data; they are echoes of past actions, whispers of forgotten tasks, or vibrant signals of recent activity. The `nightly-echo-mapper` is your sonic scanner, designed to detect these temporal echoes within your file system. It helps you distinguish between the 'fresh echoes' of recently modified files and the 'faint echoes' of long-dormant data, guiding your digital scavenging and maintenance efforts.

## Practical Utility

This utility is a high-performance command-line tool written in Rust that allows you to quickly identify files based on their last modification timestamp. It's invaluable for:

*   **Codebase Hygiene**: Find recently changed files for review or identify old, untouched files that might be candidates for archival or deletion.
*   **System Monitoring**: Spot configuration files or logs that have been unexpectedly modified or, conversely, haven't been updated when they should have been.
*   **Data Management**: Locate files that are either actively being worked on or have been forgotten for a long time.
*   **Security Audits**: Pinpoint files that have been modified within a suspicious timeframe.

## Installation

To install `nightly-echo-mapper`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/) for instructions.

```bash
cargo install nightly-echo-mapper
```

This will compile and install the `nightly-echo-mapper` binary to your Cargo bin directory (usually `~/.cargo/bin`). Ensure this directory is in your system's PATH.

## Usage

```bash
nightly-echo-mapper [OPTIONS]
```

### Options:

*   `--path <DIR>`: The directory to scan for echoes. Defaults to the current directory (`.`).
*   `--fresh <DURATION>`: Lists files modified *within* the specified duration. Examples: `1h`, `7d`, `2w`, `30m`.
*   `--stale <DURATION>`: Lists files *not modified for at least* the specified duration. Examples: `1d`, `3w`, `6M` (months), `1y` (year).
*   `--max-depth <N>`: Maximum depth to traverse directories. `0` for current directory only, `1` for current + direct children, etc. Defaults to unlimited depth.
*   `-h`, `--help`: Print help information.
*   `-V`, `--version`: Print version information.

### Examples:

1.  **Find all files modified in the last 24 hours in the current directory:**
    ```bash
    nightly-echo-mapper --fresh 1d
    ```

2.  **Find all files not modified for at least 3 months in a specific project directory:**
    ```bash
    nightly-echo-mapper --path /path/to/my/project --stale 3M
    ```

3.  **Find recently touched files, but only in the top-level and immediate subdirectories:**
    ```bash
    nightly-echo-mapper --fresh 1h --max-depth 1
    ```

4.  **List files modified in the last 30 minutes in your home directory:**
    ```bash
    nightly-echo-mapper --path ~/ --fresh 30m
    ```

## Duration Formats

The `--fresh` and `--stale` options accept human-readable durations. Valid units include:

*   `s` (seconds)
*   `m` (minutes)
*   `h` (hours)
*   `d` (days)
*   `w` (weeks)
*   `M` (months - approximately 30 days)
*   `y` (years - approximately 365 days)

Examples: `1h30m`, `2d`, `1w`, `6M`, `1y`.

## Development

To build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-echo-mapper
cargo build --release
```

The executable will be located at `target/release/nightly-echo-mapper`.
