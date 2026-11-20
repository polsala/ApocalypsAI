# Nightly Temporal Text Purifier

A high-performance CLI tool crafted in Rust to cleanse your text files of 'temporal noise' and imbue them with a unique 'temporal signature'. This utility helps maintain the pristine integrity of your textual data by removing common inconsistencies.

## Features

*   **Temporal Noise Removal**: Automatically removes empty lines, trims leading/trailing whitespace from each line, and eliminates consecutive duplicate lines.
*   **Temporal Signature Generation**: Computes a SHA256 hash of the purified content, providing a unique 'temporal signature' for integrity verification.
*   **Signature Verification**: Allows you to check a file's current temporal signature against a previously generated one to detect any alterations.
*   **Efficient**: Built with Rust for speed and reliability, suitable for large text files.

## Installation

To install the `nightly-temporal-text-purifier` CLI tool, you need to have Rust and Cargo installed on your system. If you don't, please visit [rustup.rs](https://rustup.rs/) for installation instructions.

1.  **Clone the repository (or navigate to the utility's directory):**

    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-temporal-text-purifier
    ```

2.  **Build and install the utility:**

    ```bash
    cargo install --path .
    ```

    This command compiles the project and installs the `nightly-temporal-text-purifier` executable into your Cargo bin directory (usually `~/.cargo/bin`), making it available in your system's PATH.

## Usage

```bash
nightly-temporal-text-purifier --help
```

```
Usage: nightly-temporal-text-purifier --input <INPUT> [--output <OUTPUT>] [--check-signature <CHECK_SIGNATURE>]

Purifies text files by removing temporal noise and generates a unique temporal signature.

Options:
  -i, --input <INPUT>              Input file path
  -o, --output <OUTPUT>            Output file path (optional, defaults to stdout)
  -c, --check-signature <CHECK_SIGNATURE>
                                   Check the temporal signature against a provided hash
  -h, --help                       Print help
  -V, --version                    Print version
```

### Examples

1.  **Purify a file and print to stdout:**

    ```bash
    nightly-temporal-text-purifier -i messy_log.txt
    ```

    This will print the purified content to your console, followed by its temporal signature.

2.  **Purify a file and save to a new file:**

    ```bash
    nightly-temporal-text-purifier -i raw_data.txt -o purified_data.txt
    ```

    The purified content will be saved to `purified_data.txt`, and the temporal signature will be printed to the console.

3.  **Purify a file and verify its signature:**

    First, purify and get the signature:

    ```bash
    nightly-temporal-text-purifier -i important_doc.txt -o clean_doc.txt
    # Temporal Signature: 5f4dcc3b5aa765d61d8327deb882cf99
    ```

    Later, to check if `clean_doc.txt` has been altered:

    ```bash
    nightly-temporal-text-purifier -i clean_doc.txt --check-signature 5f4dcc3b5aa765d61d8327deb882cf99
    # Temporal Signature: 5f4dcc3b5aa765d61d8327deb882cf99
    # Signature check: SUCCESS! The file's temporal integrity is stable.
    ```

    If the file has been altered, it will report a FAILED status.

## Development

To run tests:

```bash
cargo test
```

To build the project:

```bash
cargo build
```

To run the executable directly:

```bash
./target/debug/nightly-temporal-text-purifier -i <input_file>
```
