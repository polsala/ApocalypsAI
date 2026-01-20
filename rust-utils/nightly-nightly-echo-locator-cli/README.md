# nightly-echo-locator-cli

A blazing-fast fuzzy file and directory locator, echoing paths that resonate with your search.
Navigate the digital wasteland with precision, finding files and directories even when their names are but a distant whisper.

## Features

*   **Fuzzy Matching**: Find files and directories even with partial or misspelled patterns.
*   **High Performance**: Written in Rust for speed and efficiency, ideal for large directories.
*   **Simple CLI**: Easy to use from your terminal.

## Installation

1.  **Prerequisites**: Ensure you have Rust and Cargo installed. If not, visit [rustup.rs](https://rustup.rs/).
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-echo-locator-cli
    ```
3.  **Build and Install**:
    ```bash
    cargo install --path .
    ```
    This will install `echo-locator` to your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage

```bash
echo-locator <pattern> [path]
```

*   `<pattern>`: The fuzzy pattern to search for.
*   `[path]`: (Optional) The directory to start searching from. Defaults to the current directory (`.`).

### Examples

Search for "report" in the current directory:
```bash
echo-locator report
```

Search for "config" within the `/etc` directory:
```bash
echo-locator config /etc
```

Find a file named "my_important_document.pdf" with a fuzzy match:
```bash
echo-locator impdoc .
```

## Development

To run tests:
```bash
cargo test
```

To build:
```bash
cargo build
```
