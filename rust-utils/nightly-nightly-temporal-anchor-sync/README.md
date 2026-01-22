# Nightly Temporal Anchor Synchronizer

This utility ensures your system's clock is synchronized with a reliable Network Time Protocol (NTP) server. In the chaotic aftermath of temporal anomalies, maintaining a consistent timeline is paramount for any surviving infrastructure.

## Features

*   Synchronizes system time with a user-specified NTP server.
*   Provides a simple command-line interface.
*   Written in Rust for performance and reliability.

## Installation

1.  **Prerequisites**: Ensure you have Rust and Cargo installed.
    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```

2.  **Build from source**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/utils/nightly-temporal-anchor-sync
    cargo build --release
    ```

## Usage

Run the synchronizer with the desired NTP server address:

```bash
./target/release/nightly-temporal-anchor-sync <ntp_server_address>
```

**Example**:

```bash
./target/release/nightly-temporal-anchor-sync pool.ntp.org
```

## Testing

Automated tests are included to verify the functionality without requiring an actual NTP server connection.

```bash
cd utils/nightly-temporal-anchor-sync
cargo test
```
