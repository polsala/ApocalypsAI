# Nightly Echo De-Noiser

`nightly-echo-de-noiser` is a high-performance Rust command-line utility designed to filter out repetitive 'noise' and predefined patterns from text streams or log files. In the post-apocalyptic soundscape, where the void constantly whispers and echoes, this tool helps you discern the truly significant messages from the mundane static.

It can filter lines based on regular expressions and optionally remove consecutive duplicate lines, making your data streams cleaner and more focused.

## Features

*   **Regex Filtering**: Define multiple regular expressions to identify and remove 'noise' lines.
*   **Duplicate Line Suppression**: Optionally remove consecutive duplicate lines to reduce redundancy.
*   **High Performance**: Written in Rust for speed and efficiency, suitable for large log files or real-time stream processing.
*   **Flexible Input**: Reads from standard input or a specified file.

## Installation

To install `nightly-echo-de-noiser`, you need Rust and Cargo installed. If you don't have them, follow the instructions on [rust-lang.org](https://www.rust-lang.org/tools/install).

```bash
cargo install nightly-echo-de-noiser
```

Alternatively, you can clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-echo-de-noiser
cargo build --release
# The executable will be in target/release/nightly-echo-de-noiser
```

## Usage

```bash
nightly-echo-de-noiser [OPTIONS] [FILE]
```

### Arguments

*   `<FILE>`: Optional. The path to the input file. If not provided, input is read from stdin.

### Options

*   `-p, --pattern <REGEX>`: One or more regular expressions to treat as 'noise'. Lines matching any of these patterns will be filtered out. Can be specified multiple times.
*   `-d, --deduplicate`: Enable filtering of consecutive duplicate lines.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

## Examples

1.  **Filter out specific log messages from a file:**

    ```bash
    nightly-echo-de-noiser -p "^INFO: Heartbeat received" -p "^DEBUG: Processing request" /var/log/apocalypse-sentry.log
    ```

2.  **De-noise a streaming input, removing empty lines and duplicates:**

    ```bash
    cat /var/log/void-whispers.log | nightly-echo-de-noiser -p "^$" -d
    ```

3.  **Filter multiple patterns and deduplicate from stdin:**

    ```bash
    echo -e "Void echo 1\nVoid echo 1\nStatic hum\nImportant message\nStatic hum" | nightly-echo-de-noiser -p "Static hum" -d
    # Expected output:
    # Void echo 1
    # Important message
    ```

## Development

To run tests:

```bash
cargo test
```
