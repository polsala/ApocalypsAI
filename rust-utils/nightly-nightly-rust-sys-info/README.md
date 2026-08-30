# nightly-rust-sys-info

A whimsical yet useful standalone utility built with Rust. This CLI tool provides a quick and efficient way to gather and display essential system information.

## Features

*   **CPU Information**: Displays CPU model, cores, and frequency.
*   **Memory Usage**: Shows total, used, and free RAM.
*   **Disk Usage**: Lists mounted filesystems, their total size, used space, and mount points.
*   **OS Information**: Provides the operating system name and version.

## Installation

1.  **Prerequisites**: Ensure you have Rust and Cargo installed.
    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```

2.  **Build from Source**: Clone the repository and build the utility.
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

Run the utility from your terminal:

```bash
nightly-rust-sys-info
```

## Development & Testing

This utility is built using Rust and includes comprehensive unit tests.

To run the tests:

```bash
cd rust-utils/nightly-rust-sys-info
cargo test
```

## Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.
