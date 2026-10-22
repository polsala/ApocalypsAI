## nightly-rust-sys-monitor

A whimsical yet useful standalone utility built with Rust. This CLI tool provides a high-performance, low-overhead way to monitor key system resource usage metrics: CPU utilization, memory consumption, and disk I/O.

### Philosophy

Inspired by the need for efficient monitoring in resource-constrained or performance-critical environments, this tool prioritizes speed and minimal system impact. It's designed to be a reliable companion for sysadmins, developers, and anyone curious about their system's heartbeat.

### Features

*   **Real-time CPU Usage**: Displays current CPU utilization percentage.
*   **Memory Usage**: Shows total, used, and free memory in a human-readable format.
*   **Disk I/O**: Reports read and write speeds for the primary disk.
*   **Low Overhead**: Written in Rust for maximum performance and minimal resource footprint.
*   **Simple CLI Interface**: Easy to run and interpret.

### Installation

Ensure you have Rust and Cargo installed.

1.  Clone this repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```

2.  Navigate to the utility's directory:
    ```bash
    cd rust-utils/nightly-rust-sys-monitor
    ```

3.  Build the project:
    ```bash
    cargo build --release
    ```

### Usage

After building, you can run the monitor from the `target/release/` directory:

```bash
./nightly-rust-sys-monitor
```

Or, if you've installed it globally (e.g., via `cargo install --path .`), you can run it from anywhere:

```bash
nightly-rust-sys-monitor
```

**Example Output:**

```
System Monitor Report:
--------------------
CPU Usage: 15.2%
Memory Usage: 4.5 GB / 16.0 GB (28.1%)
Disk Read: 12.3 MB/s
Disk Write: 8.9 MB/s
```

### Development & Testing

This utility is built with Rust and includes comprehensive unit tests. You can run the tests using:

```bash
cargo test
```

### Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.
