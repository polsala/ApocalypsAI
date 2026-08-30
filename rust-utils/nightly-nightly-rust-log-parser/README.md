# nightly-rust-log-parser

A whimsical yet useful standalone utility for the ApocalypsAI community. This tool is a high-performance Command Line Interface (CLI) application written in Rust, designed to efficiently parse and filter structured log entries. It's perfect for sifting through the digital detritus of any apocalyptic scenario.

## Features

*   **Fast Parsing**: Leverages Rust's performance to quickly process large log files.
*   **Structured Log Support**: Designed to understand common structured log formats (e.g., JSON).
*   **Flexible Filtering**: Allows users to filter logs based on keywords, log levels, or custom patterns.
*   **Standalone Executable**: Compiles into a single, self-contained binary.

## Installation

To install, you'll need Rust and Cargo. Clone this repository and run:

```bash
cd utils/nightly-rust-log-parser
cargo install --path .
```

## Usage

Once installed, you can use the `nightly-rust-log-parser` command:

```bash
# Parse a log file and filter for lines containing 'error'
cat my_apocalypse.log | nightly-rust-log-parser --filter "error"

# Parse a JSON log file and filter for lines with level 'WARN'
cat structured_logs.json | nightly-rust-log-parser --format json --filter "level:WARN"

# Show help message
nightly-rust-log-parser --help
```

## Configuration

Currently, filtering is done via command-line arguments. Future versions might support configuration files.

## Testing

All tests are included and can be run using Cargo:

```bash
cd utils/nightly-rust-log-parser
cargo test
```

## Contributing

Contributions are welcome! Please follow the ApocalypsAI contribution guidelines.
