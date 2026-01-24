# Nightly Void-Whisper Filter

A high-performance command-line utility crafted in Rust to help you tune into the subtle 'void whispers' – specific keywords or regex patterns – hidden within vast streams of text data. Whether you're sifting through ancient logs, monitoring real-time data feeds, or analyzing cryptic messages, this tool helps you pinpoint and contextualize the signals that matter.

## Features

*   **Blazing Fast**: Leverages Rust's performance for efficient text processing.
*   **Regex Support**: Search using powerful regular expressions.
*   **Streaming Input**: Works seamlessly with `stdin` or files, making it pipeline-friendly.
*   **Contextual Output**: Display lines preceding a match to provide crucial context.
*   **Match Count**: Reports the total number of 'void whispers' found.

## Installation

To use the Nightly Void-Whisper Filter, you'll need the Rust toolchain installed. If you don't have it, you can install it via `rustup`:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
```

Once Rust is installed, you can build and install the utility from the repository:

```bash
# Clone the ApocalypsAI repository (if you haven't already)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-void-whisper-filter

# Build and install
cargo install --path .
```

This will install the `void-whisper-filter` executable to your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage

```bash
void-whisper-filter [OPTIONS]
```

### Arguments

*   `-p`, `--pattern <PATTERN>`: **Required**. The regex pattern to search for (the 'void whisper').
*   `-f`, `--file <FILE>`: Path to the input file. If not provided, reads from `stdin`.
*   `-c`, `--context <CONTEXT_LINES>`: Number of context lines to show *before* each match. Defaults to `0`.

### Examples

1.  **Find all occurrences of "ERROR" in a log file:**

    ```bash
    void-whisper-filter --pattern "ERROR" --file /var/log/syslog
    ```

2.  **Search for IP addresses in a stream from `stdin` and show 2 preceding lines of context:**

    ```bash
    cat access.log | void-whisper-filter -p "\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}" -c 2
    ```

3.  **Find specific anomaly codes (e.g., `ANOMALY-\d{4}`) without context:**

    ```bash
    void-whisper-filter -p "ANOMALY-\\d{4}" < sensor_data.txt
    ```

4.  **Case-insensitive search for a keyword (using regex flags):**

    ```bash
    void-whisper-filter -p "(?i)critical" --file application.log
    ```

## Development

To run tests:

```bash
cargo test
```

To build the project:

```bash
cargo build
```
