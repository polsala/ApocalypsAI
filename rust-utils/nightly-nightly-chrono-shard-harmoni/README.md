# Nightly Chrono-Shard Harmonizer

The cosmos is a chaotic place, and sometimes, even the most meticulously logged temporal data can suffer from fragmentation, echoes, and outright rifts. The `nightly-chrono-shard-harmonizer` is your trusty Rust-powered CLI companion designed to bring order to the temporal chaos.

It processes streams of timestamped data, sorts them into a coherent timeline, and identifies anomalies:
*   **Temporal Rifts**: Significant gaps in the chronological sequence, indicating missing data shards.
*   **Echoes of Time**: Duplicate timestamps, suggesting redundant or conflicting entries.
*   **Chronological Drift**: Reports if the input data was not originally sorted.

Bring harmony back to your data streams!

## Features

*   **High Performance**: Written in Rust for blazing-fast processing of large datasets.
*   **Flexible Input**: Reads from `stdin` or a specified file.
*   **Configurable Thresholds**: Define what constitutes a "temporal rift" (gap).
*   **Detailed Report**: Outputs a summary of detected anomalies and the harmonized data.

## Installation

1.  **Prerequisites**: Ensure you have Rust and Cargo installed. If not, visit [rustup.rs](https://rustup.rs/).
2.  **Build from source**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-chrono-shard-harmonizer
    cargo build --release
    ```
3.  **Run**: The executable will be found at `target/release/chrono-shard-harmonizer`. You can copy it to your `PATH` for easy access.

## Usage

```bash
chrono-shard-harmonizer [OPTIONS] [FILE]
```

### Arguments

*   `<FILE>`: Optional. Path to the input file. If not provided, reads from `stdin`.

### Options

*   `-t, --gap-threshold <SECONDS>`: Define the maximum allowed time difference (in seconds) between consecutive entries before it's considered a "Temporal Rift". Default is `60` seconds.
*   `-f, --timestamp-format <FORMAT>`: Specify the timestamp format. Uses `RFC3339` by default (e.g., `2023-01-01T10:00:00Z`). Currently, only `RFC3339` is fully supported for robust parsing. Other formats will attempt RFC3339 parsing with a warning.
*   `-o, --output-harmonized`: Output the harmonized (sorted and de-duplicated by timestamp) data to stdout. By default, only the anomaly report is printed.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

## Examples

1.  **Harmonize data from a file, default gap threshold:**
    ```bash
    chrono-shard-harmonizer my_log_data.txt
    ```

2.  **Process data from stdin, custom gap threshold, output harmonized data:**
    ```bash
    cat sensor_readings.log | chrono-shard-harmonizer -t 300 -o
    ```

3.  **Generate a report only, with a very strict gap threshold:**
    ```bash
    echo "2023-01-01T10:00:00Z Data A" > temp_data.log
    echo "2023-01-01T10:00:01Z Data B" >> temp_data.log
    echo "2023-01-01T10:00:03Z Data C" >> temp_data.log
    echo "2023-01-01T10:00:03Z Data D" >> temp_data.log # Echo
    echo "2023-01-01T10:00:10Z Data E" >> temp_data.log # Gap
    chrono-shard-harmonizer temp_data.log -t 2
    ```

    Expected output (simplified):
    ```
    Harmonization Report:
    ---------------------
    Input lines processed: 5
    Valid data shards found: 5
    Original order: Chronological Drift Detected (1 out-of-order instances)
    Echoes of Time (Duplicate Timestamps): 1
      - 2023-01-01T10:00:03Z (2 occurrences)
    Temporal Rifts (Gaps > 2s): 1
      - Rift detected between 2023-01-01T10:00:03Z and 2023-01-01T10:00:10Z (Duration: 7s)
    ```
