# Nightly Log Echo Compressor

A high-performance Rust CLI tool designed to combat 'temporal echoes' in log files by compressing repetitive entries. This utility helps improve log readability and reduces file size by replacing consecutive identical or near-identical lines (optionally ignoring timestamps) with a single entry and a repetition count.

## Features

*   **Efficient Log Compression**: Identifies and consolidates repeated log lines.
*   **Timestamp Agnostic Comparison**: Optionally ignores timestamps using a configurable regular expression for more effective de-duplication.
*   **CLI Interface**: Easy to use from the command line.
*   **Rust Performance**: Built with Rust for speed and memory efficiency, suitable for large log files.

## Installation

To build and install the `nightly-log-echo-compressor` from source, you'll need Rust and Cargo installed.

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-log-echo-compressor
cargo build --release
# The executable will be found at target/release/nightly-log-echo-compressor
# You might want to add it to your PATH or copy it to a bin directory.
```

## Usage

```bash
nightly-log-echo-compressor [OPTIONS] <INPUT_FILE>
```

### Arguments

*   `<INPUT_FILE>`: The path to the log file to be processed.

### Options

*   `-o, --output <OUTPUT_FILE>`: Path to the output file. If not specified, output will be printed to stdout.
*   `-r, --regex <REGEX_PATTERN>`: A regular expression pattern to identify and strip timestamps or other variable parts from log lines before comparison. The matched part will be ignored for de-duplication, but the original line (or the first occurrence's line) will be printed.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

## Examples

1.  **Compress a log file to stdout without ignoring timestamps:**

    ```bash
    nightly-log-echo-compressor my_app.log
    ```

2.  **Compress a log file and save the output to a new file, ignoring timestamps:**

    Assuming timestamps look like `[YYYY-MM-DD HH:MM:SS]`, you might use a regex like `^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] `.

    ```bash
    nightly-log-echo-compressor my_app.log -o compressed_app.log -r "^\\[\\d{{4}}-\\d{{2}}-\\d{{2}} \\d{{2}}:\\d{{2}}:\\d{{2}}\\] "
    ```
    *Note the double backslashes in the regex when passed via command line to escape them for the shell and then for the regex engine.*

3.  **Compress a log file with a more generic timestamp/ID regex:**

    If your logs have `[INFO] [Thread-123] Message`, and you want to ignore `[Thread-123]`:

    ```bash
    nightly-log-echo-compressor server.log -r "\\[Thread-\\d+\\] "
    ```

## How it Works

The tool reads the input log file line by line. It keeps track of the last unique line encountered and a count of how many times it has consecutively appeared. When a new, different line is found (after optionally stripping parts matched by the regex), the previous unique line and its count are written to the output. This process continues until the end of the file.

For lines where a regex is provided, the comparison is performed on the 'stripped' version of the line. However, the *original* first occurrence of the line (including its timestamp/variable part) is preserved in the output, followed by the repetition count.
