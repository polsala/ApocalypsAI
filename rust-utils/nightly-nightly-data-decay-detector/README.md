# Nightly Data Decay Detector

## Summary
`nightly-data-decay-detector` is a whimsical-yet-useful command-line utility built in Rust. It scans specified directories to identify files that haven't been accessed or modified recently, assigning them a 'decay score'. The higher the score, the more 'dusty' or forgotten the file is, suggesting it might be a candidate for archival, deletion, or simply a review to see if it's still relevant.

Think of it as a digital dustbunny sweeper for your file system, helping you keep your data fresh and organized in the face of digital entropy.

## Features
- **Fast Scanning**: Leverages Rust's performance for quick directory traversal.
- **Decay Scoring**: Calculates a 'decay score' based on last modification and access times.
- **Configurable Threshold**: Filter files by a minimum decay score.
- **Configurable Sorting**: Sort results by decay score, modification time, or access time.
- **Human-Readable Output**: Displays file paths, decay scores, and timestamps.

## Installation

To install `nightly-data-decay-detector`, you need Rust and Cargo installed. If you don't have them, visit [rustup.rs](https://rustup.rs/).

```bash
cargo install nightly-data-decay-detector
```

## Usage

```bash
nightly-data-decay-detector [OPTIONS] <PATH>
```

### Arguments
- `<PATH>`: The directory to scan for decaying files.

### Options
- `-t, --threshold <THRESHOLD>`: Only show files with a decay score equal to or higher than this value. Default is `0.0` (show all).
- `-s, --sort-by <FIELD>`: Sort output by 'decay' (descending), 'mtime' (ascending), or 'atime' (ascending). Default is 'decay'.
- `-l, --limit <LIMIT>`: Limit the number of results displayed. Default is `0` (no limit).
- `-v, --verbose`: Show more detailed timestamps (including time of day).
- `-h, --help`: Print help information.

### Decay Score Calculation
The decay score is a floating-point number representing the 'age' of a file's inactivity. It's primarily based on the number of days since the file was last modified, with a slight influence from the last access time. Specifically:

`Decay Score = (Days Since Last Modified * 0.8) + (Days Since Last Accessed * 0.2)`

A higher score indicates a file that has been untouched for a longer period.

## Examples

Scan the current directory and show all files with a decay score:
```bash
nightly-data-decay-detector .
```

Show files in `/var/log` that haven't been touched in over 30 days (approx. decay score 30):
```bash
nightly-data-decay-detector /var/log --threshold 30.0
```

Find the top 10 most decayed files in your home directory, sorted by modification time (oldest first):
```bash
nightly-data-decay-detector ~/ --limit 10 --sort-by mtime
```

## Development

To build from source:
```bash
cargo build --release
```

To run tests:
```bash
cargo test
```
