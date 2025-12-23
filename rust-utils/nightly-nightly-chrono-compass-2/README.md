# Nightly Chrono-Compass

## Temporal Drift Locator

In the ever-shifting sands of the post-apocalyptic digital wasteland, file system timestamps can become... peculiar. The `nightly-chrono-compass` is your trusty Rust-powered CLI tool designed to detect and pinpoint these temporal anomalies, revealing files whose modification or creation dates are suspiciously out of sync with their surroundings.

Think of it as a Geiger counter for time, clicking louder as you approach a pocket of chronal instability. Whether it's a forgotten backup, a corrupted file, or the subtle signature of a temporal intruder, the Chrono-Compass will guide you.

## Features

*   **High-Performance Scan**: Leverages Rust's speed for rapid traversal of large directories.
*   **Local Anomaly Detection**: Identifies files whose timestamps deviate significantly from the median of their immediate directory.
*   **Configurable Threshold**: Set how sensitive your compass is to temporal ripples.
*   **Whimsical Output**: Reports anomalies with a "Temporal Resonance" score, guiding you to the heart of the time-drift.

## Installation

Ensure you have Rust and Cargo installed. Then, you can build and run:

```bash
cargo build --release
./target/release/chrono-compass --help
```

Or, if published to crates.io (not yet):

```bash
cargo install nightly-chrono-compass
```

## Usage

```bash
chrono-compass <PATH> [OPTIONS]
```

**Arguments:**

*   `<PATH>`: The directory to scan for temporal anomalies.

**Options:**

*   `-t, --threshold <SECONDS>`: The maximum allowed deviation in seconds from the median timestamp of a directory's files. Files exceeding this threshold will be flagged. (Default: 3600 seconds / 1 hour)
*   `-m, --mode <MODE>`: Which timestamp to analyze. Can be `mtime` (modification time) or `ctime` (creation time). (Default: `mtime`)
*   `-v, --verbose`: Show more detailed output, including median timestamps.
*   `-h, --help`: Print help information.

## Examples

Scan the current directory for files with modification times deviating by more than 2 hours:

```bash
chrono-compass . --threshold 7200
```

Scan a specific archive directory for creation time anomalies, with verbose output:

```bash
chrono-compass /var/log/old_archives --mode ctime -v
```

## Output Interpretation

When a temporal anomaly is detected, the Chrono-Compass will emit a reading like this:

```
[Temporal Resonance Detected] File: /path/to/your/file.txt
  Timestamp Type: mtime
  File Time: 2023-10-26 14:30:00 UTC
  Local Median: 2023-10-26 15:00:00 UTC
  Chronal Drift: -1800 seconds (30 minutes) - SIGNIFICANT!
```

A positive drift means the file is newer than its peers, a negative drift means it's older. The magnitude indicates the strength of the temporal ripple.
