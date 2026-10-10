# nightly-rust-sys-monitor

A whimsical yet useful standalone utility for the ApocalypsAI community. This tool is a high-performance Command Line Interface (CLI) application written in Rust, designed to monitor essential system resource usage with minimal overhead.

## Features

*   **CPU Usage**: Real-time percentage of CPU utilization.
*   **Memory Usage**: Current RAM usage (total, used, free, and percentage).
*   **Disk I/O**: Read and write operations per second for the primary disk.
*   **Low Overhead**: Optimized for minimal system impact, making it suitable for continuous monitoring.
*   **Human-Readable Output**: Displays resource metrics in an easy-to-understand format.

## Installation

Ensure you have Rust and Cargo installed. If not, follow the official Rust installation guide:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Then, clone this repository and build the utility:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI
cd rust-utils/nightly-rust-sys-monitor
cargo build --release
```

The executable will be located in `target/release/nightly-rust-sys-monitor`.

## Usage

Run the utility from your terminal:

```bash
./target/release/nightly-rust-sys-monitor
```

By default, it will display the system resource usage every second. You can specify an update interval in seconds:

```bash
./target/release/nightly-rust-sys-monitor <interval_in_seconds>
```

For example, to update every 5 seconds:

```bash
./target/release/nightly-rust-sys-monitor 5
```

## How it Works

This utility leverages Rust's powerful system interaction capabilities and external crates like `sysinfo` to gather system metrics. It's designed to be efficient and provide a clear, concise overview of your system's health.

## Testing

Automated tests are included to ensure the core functionality works as expected. Run tests using Cargo:

```bash
cd rust-utils/nightly-rust-sys-monitor
cargo test
```
