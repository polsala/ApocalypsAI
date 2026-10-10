# nightly-rust-sysinfo-cli

A whimsical yet useful standalone utility built with Rust. This CLI tool provides a quick and efficient way to retrieve essential system information.

## Features

*   Displays CPU usage and load.
*   Shows memory (RAM) usage.
*   Lists network interface statistics.
*   Provides disk usage information.

## Installation

Ensure you have Rust and Cargo installed.

```bash
cargo install --git https://github.com/polsala/ApocalypsAI.git --branch main rust-utils/nightly-rust-sysinfo-cli
```

## Usage

Run the command from your terminal:

```bash
nightly-rust-sysinfo-cli
```

## Development

To build and run locally:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-rust-sysinfo-cli
cargo build --release
cargo run --release
```

## Testing

Run the included tests:

```bash
cargo test
```
