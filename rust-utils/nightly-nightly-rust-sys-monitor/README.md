# nightly-rust-sys-monitor

A whimsical yet useful Rust CLI tool for monitoring system resource usage. Inspired by the need to keep our digital fortresses operational even in the face of the apocalypse, this tool provides a quick, high-performance overview of your system's vital signs.

## Features

*   **CPU Usage**: Tracks overall CPU utilization.
*   **Memory Usage**: Monitors RAM consumption (total, used, free).
*   **Disk Usage**: Reports on the health and capacity of your storage.
*   **Fast & Efficient**: Built with Rust for maximum performance and minimal overhead.
*   **Apocalyptic Flair**: Output is presented with a touch of post-apocalyptic charm.

## Installation

Ensure you have Rust and Cargo installed.

```bash
cargo install --git https://github.com/polsala/ApocalypsAI.git --branch main --path utils/nightly-rust-sys-monitor
```

## Usage

Run the tool from your terminal:

```bash
nightly-rust-sys-monitor
```

## Example Output

```
--- System Status Report ---

CPU Core 0: 15.2% utilized.  (Whispering winds of data)
CPU Core 1: 22.8% utilized.  (Echoes of computation)
CPU Core 2: 18.5% utilized.  (The hum of survival)
CPU Core 3: 25.1% utilized.  (Guardians of the network)

Total Memory: 16.0 GB
Used Memory:  8.5 GB (53.1%)
Free Memory:  7.5 GB (46.9%)
(Sustaining the digital sanctuary)

Disk: /dev/sda1 (Root)
Total Space:  500.0 GB
Used Space:   250.0 GB (50.0%)
Free Space:   250.0 GB (50.0%)
(The last bastion of data)

--- End Report ---
```

## Development & Testing

This utility is built using Rust. Tests are included and can be run with `cargo test`.

```bash
cd utils/nightly-rust-sys-monitor
cargo test
```
