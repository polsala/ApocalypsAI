# nightly-signal-whisperer

A high-performance CLI tool that scans text-based "signals" (input files or stdin) for anomalous patterns, repeating sequences, and predefined keywords, whispering potential insights into the data. Perfect for post-apocalyptic data forensics or just finding hidden messages in noisy streams.

## Features

*   **Keyword Detection**: Quickly find specific words or phrases in the signal.
*   **Repeating Sequence Analysis**: Identify recurring patterns that might indicate structured data, codes, or distress signals.
*   **Character Frequency Anomalies**: Highlight characters that appear with unusually high frequency, potentially pointing to encoded information or data corruption.
*   **Flexible Input**: Reads from a specified file or standard input.

## Installation

To build and install `nightly-signal-whisperer`, you need Rust and Cargo installed. If you don't have them, follow the instructions at [rustup.rs](https://rustup.rs/).

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-signal-whisperer
    ```
2.  **Build the utility:**
    ```bash
    cargo build --release
    ```
    The executable will be located at `target/release/nightly-signal-whisperer`.
3.  **Optionally, install it to your Cargo bin directory:**
    ```bash
    cargo install --path .
    ```
    This will make `nightly-signal-whisperer` available in your shell's PATH.

## Usage

```
nightly-signal-whisperer [OPTIONS]
```

### Options

*   `-f`, `--file <FILE_PATH>`: Path to the signal file. If not provided, reads from stdin.
*   `-k`, `--keywords <KEYWORD1,KEYWORD2,...>`: Comma-separated list of keywords to search for.
*   `-m`, `--min-repeat-len <LENGTH>`: Minimum length for repeating sequences to be considered significant (default: 3).
*   `-t`, `--freq-threshold <PERCENTAGE>`: Character frequency threshold (as a percentage) to flag as anomalous (default: 10.0).
*   `-h`, `--help`: Print help information.
*   `-V`, `--version`: Print version information.

### Examples

1.  **Scan a file for specific keywords:**
    ```bash
    nightly-signal-whisperer -f signal.txt -k "SOS,shelter,coordinates"
    ```
2.  **Analyze stdin for repeating patterns and high-frequency characters:**
    ```bash
    echo "This is a test. test test test. AAAAAABBC" | nightly-signal-whisperer -m 4 -t 20.0
    ```
3.  **Combine all features on a file:**
    ```bash
    nightly-signal-whisperer -f complex_signal.log -k "anomaly,danger" -m 5 -t 15.0
    ```

## Development

### Running Tests

To run the automated tests, navigate to the utility's directory and execute:

```bash
cargo test
```

### Project Structure

```
.
├── Cargo.toml
├── README.md
├── src/
│   └── main.rs
└── tests/
    └── integration_test.rs
```
