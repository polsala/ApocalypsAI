# Nightly Temporal Drift Detector (nightly-temporal-drift-detect)

## Overview

The `nightly-temporal-drift-detect` is a high-performance command-line utility crafted in Rust to scan your filesystem for files exhibiting unusual temporal anomalies in their modification and creation timestamps. In the chaotic post-apocalyptic landscape, maintaining data integrity and understanding system state is paramount. This tool helps identify files whose last modification time (`mtime`) is in the future, or whose `mtime` is inexplicably older than their creation time (`ctime`), signaling potential clock synchronization issues, filesystem corruption, or even subtle temporal distortions.

## Features

*   **Future `mtime` Detection**: Flags files whose modification timestamp is set to a time in the future relative to the current system clock.
*   **`mtime` Older Than `ctime` Detection**: Identifies files where the last modification time precedes the file's creation time, a highly unusual and often indicative anomaly.
*   **Recursive Scanning**: Traverses directories recursively to check all files.
*   **Configurable Thresholds**: Allows setting a tolerance for future `mtime` detection.
*   **Fast & Efficient**: Built with Rust for optimal performance on large filesystems.

## Installation

To install `nightly-temporal-drift-detect`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/) for instructions.

```bash
cargo install nightly-temporal-drift-detect
```

Alternatively, you can clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-temporal-drift-detect
cargo build --release
# The executable will be found at target/release/nightly-temporal-drift-detect
```

## Usage

Run the utility from your terminal:

```bash
nightly-temporal-drift-detect [OPTIONS] <PATH>
```

### Arguments

*   `<PATH>`: The root directory to start scanning from. Defaults to the current directory if not provided.

### Options

*   `-f, --future-threshold <SECONDS>`: Tolerance in seconds for `mtime` being in the future. Files with `mtime` up to `SECONDS` in the future will be ignored. Default is `0` (any future `mtime` is an anomaly).
*   `-v, --verbose`: Enable verbose output, showing all files scanned (not just anomalies).
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

### Examples

Scan the current directory for temporal drifts:

```bash
nightly-temporal-drift-detect .
```

Scan a specific directory, allowing `mtime`s up to 5 seconds in the future:

```bash
nightly-temporal-drift-detect /var/log --future-threshold 5
```

Scan your home directory with verbose output:

```bash
nightly-temporal-drift-detect ~/documents -v
```

## Output

The tool will print detected anomalies to `stdout` in a human-readable format, indicating the file path and the type of temporal drift detected.

Example output:

```
Temporal Anomaly Detected: "./future_file.txt" - mtime is in the future (2024-12-31 23:59:59 UTC)
Temporal Anomaly Detected: "./past_mtime_file.txt" - mtime (2020-01-01 00:00:00 UTC) is older than ctime (2023-05-15 10:00:00 UTC)
```
