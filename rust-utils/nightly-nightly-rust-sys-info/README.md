# nightly-rust-sys-info

A whimsical yet useful standalone utility built with Rust. This CLI tool provides a quick and efficient way to gather and display essential system information.

## Features

*   **CPU Usage**: Real-time CPU utilization percentage.
*   **Memory Usage**: Total, used, and free RAM.
*   **Disk Usage**: Free space on the root partition.
*   **Uptime**: How long the system has been running.
*   **Hostname**: The system's network name.

## Installation

1.  **Prerequisites**: Ensure you have Rust and Cargo installed.
    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```

2.  **Build from source**: Clone the repository and build the utility.
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-rust-sys-info
    cargo build --release
    ```

3.  **Run**: Execute the compiled binary.
    ```bash
    ./target/release/nightly-rust-sys-info
    ```

## Usage

Run the tool from your terminal:

```bash
nightly-rust-sys-info
```

## Example Output

```
System Information:
-------------------
Hostname: my-apocalypse-server
Uptime:   2 days, 5 hours, 30 minutes
CPU Usage: 15.2%
Memory Usage: 4.5 GB / 16.0 GB (Used: 28.1%)
Disk Usage (root): 150 GB free
```

## Development & Testing

This utility is built using Rust and leverages the `sysinfo` crate for cross-platform system information retrieval.

To run the tests:

```bash
cd rust-utils/nightly-rust-sys-info
cargo test
```
