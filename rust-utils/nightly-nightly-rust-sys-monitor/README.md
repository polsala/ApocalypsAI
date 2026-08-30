# nightly-rust-sys-monitor

A whimsical yet useful standalone utility for the ApocalypsAI community. This tool is a high-performance command-line interface (CLI) application written in Rust, designed to monitor key system resource usage: CPU, memory, and disk I/O.

## Philosophy

Inspired by the need for robust and efficient system monitoring in potentially chaotic environments, this utility prioritizes speed and low overhead. Rust's performance characteristics make it ideal for such a task.

## Features

*   **Real-time CPU Usage**: Displays current CPU utilization.
*   **Memory Usage**: Shows total, used, and free RAM.
*   **Disk I/O**: Monitors read and write operations per second.
*   **Configurable Refresh Rate**: Adjust how often the data is updated.
*   **Human-Readable Output**: Presents data in an easy-to-understand format.

## Installation

Ensure you have Rust and Cargo installed.

1.  Clone the repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```

2.  Build the utility:
    ```bash
    cargo build --release
    ```

3.  The executable will be located at `target/release/nightly-rust-sys-monitor`.

## Usage

Run the utility from your terminal:

```bash
./target/release/nightly-rust-sys-monitor
```

**Options:**

*   `-i <seconds>` or `--interval <seconds>`: Set the refresh interval in seconds (default: 2).

    Example:
    ```bash
    ./target/release/nightly-rust-sys-monitor -i 5
    ```

## How it Works

The tool leverages Rust's system-level capabilities and external crates to gather information directly from the operating system. It periodically polls for updates and displays them in a clear, concise manner.

## Testing

Unit tests are included to verify the functionality of core components. To run the tests:

```bash
cargo test
```

## Contributing

Contributions are welcome! Please refer to the main ApocalypsAI repository for contribution guidelines.
