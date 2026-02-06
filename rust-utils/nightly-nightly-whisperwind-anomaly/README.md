# nightly-whisperwind-anomaly

A high-performance CLI tool crafted in Rust to detect and classify subtle environmental anomalies from sensor data. It processes numerical readings and categorizes them into whimsical yet informative classifications, providing quick, color-coded feedback on the ambient "mood" of your surroundings.

## Features

*   **Fast Processing**: Built with Rust for speed and efficiency, ideal for processing large datasets of environmental readings.
*   **Whimsical Classification**: Categorizes readings into:
    *   `Harmless Rustle` (Green)
    *   `Curious Gust` (Yellow)
    *   `Ominous Howl` (Red)
    *   `Cataclysmic Roar!` (Magenta, bold)
    *   `Unintelligible Static` (Dimmed)
*   **Flexible Input**: Reads from standard input (stdin) or a specified file.
*   **Color-Coded Output**: Provides immediate visual cues for anomaly severity.

## Installation

To build and install `nightly-whisperwind-anomaly`, you need Rust and Cargo installed. If you don't have them, visit [rustup.rs](https://rustup.rs/).

1.  **Navigate to this utility's directory:**
    ```bash
    # Assuming you are in the root of the ApocalypsAI repository
    cd rust-utils/nightly-whisperwind-anomaly
    ```
2.  **Build the project:**
    ```bash
    cargo build --release
    ```
3.  **The executable will be located at `target/release/nightly-whisperwind-anomaly`.**
    You can copy it to a directory in your `PATH` for easier access:
    ```bash
    cp target/release/nightly-whisperwind-anomaly /usr/local/bin/
    ```

## Usage

The tool can read from standard input or a file. Each line should contain a single numerical environmental reading (a floating-point number).

### Reading from Standard Input

Pipe data directly to the tool:

```bash
echo "0.1\n0.3\n0.7\n1.2\n-0.1\nnot_a_number" | nightly-whisperwind-anomaly
```

Expected Output (colors will be applied in a real terminal):
```
Reading: 0.1000   -> Harmless Rustle
Reading: 0.3000   -> Curious Gust
Reading: 0.7000   -> Ominous Howl
Reading: 1.2000   -> Cataclysmic Roar!
Reading: -0.1     -> Unintelligible Static
Reading: not_a_nu -> Unintelligible Static
```

### Reading from a File

Create a file with environmental readings, e.g., `readings.txt`:
```
0.05
0.45
0.9
1.5
0.20
0.51
invalid
```

Then run the tool with the `--file` option:

```bash
nightly-whisperwind-anomaly --file readings.txt
```

Expected Output (colors will be applied in a real terminal):
```
Reading: 0.0500   -> Harmless Rustle
Reading: 0.4500   -> Curious Gust
Reading: 0.9000   -> Ominous Howl
Reading: 1.5000   -> Cataclysmic Roar!
Reading: 0.2000   -> Harmless Rustle
Reading: 0.5100   -> Ominous Howl
Reading: invalid  -> Unintelligible Static
```

## Development and Testing

### Running Tests

To run the unit tests:

```bash
cargo test
```

### Mock Rationale

The tests are designed to be deterministic and offline. They directly call the classification logic (`Anomaly::classify`) with predefined numerical inputs and assert the expected `Anomaly` type. The `process_line` function, which handles parsing and output formatting, is tested by capturing its standard output, ensuring its behavior is consistent. The `main` function's file reading capabilities are implicitly covered by the `process_line` tests and reliance on standard library I/O, with the core logic fully unit-tested.
