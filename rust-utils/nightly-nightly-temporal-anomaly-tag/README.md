# Nightly Temporal Anomaly Tagger (nightly-temporal-anomaly-tagger)

A high-performance CLI tool built with Rust to help you quickly tag and categorize those pesky temporal anomalies, reality glitches, and spacetime distortions that keep popping up. Don't just observe them, *classify* them!

## Features

*   **Fast & Efficient**: Written in Rust for blazing-fast anomaly tagging.
*   **Categorization**: Assign specific types (Echo, Warp, Flicker, Loop, Glitch, Phantom, Shift) to your observations.
*   **Severity Rating**: Mark anomalies by their impact (Trivial, Minor, Moderate, Severe, Critical).
*   **Structured Output**: Generates a consistent, easily parsable tag for logging or further analysis.

## Installation

### Prerequisites

*   Rust toolchain (rustup recommended)

### Build from Source

1.  Navigate to the `rust-utils/nightly-temporal-anomaly-tagger` directory.
2.  Build the project:
    ```bash
    cargo build --release
    ```
3.  The executable will be located at `target/release/nightly-temporal-anomaly-tagger`. You can copy it to your `PATH` for easy access:
    ```bash
    cp target/release/nightly-temporal-anomaly-tagger /usr/local/bin/
    ```

## Usage

Run the `nightly-temporal-anomaly-tagger` command with the anomaly's description, type, and severity.

```bash
nightly-temporal-anomaly-tagger --description "My coffee cup briefly turned into a squirrel." --type Echo --severity Minor
```

### Arguments

*   `-d`, `--description <DESCRIPTION>`: A detailed account of the temporal anomaly observed. (Required)
*   `-t`, `--anomaly-type <TYPE>`: The classification of the anomaly. Choose from: `Echo`, `Warp`, `Flicker`, `Loop`, `Glitch`, `Phantom`, `Shift`. (Required)
*   `-s`, `--severity <SEVERITY>`: The perceived impact or intensity of the anomaly. Choose from: `Trivial`, `Minor`, `Moderate`, `Severe`, `Critical`. (Required)

### Examples

1.  **A minor reality flicker:**
    ```bash
    nightly-temporal-anomaly-tagger -d "The street sign briefly displayed 'Welcome to Narnia'." -t Flicker -s Minor
    # Output: [ANOMALY:Flicker|Minor] The street sign briefly displayed 'Welcome to Narnia'.
    ```

2.  **A severe time loop:**
    ```bash
    nightly-temporal-anomaly-tagger -d "I've relived this exact moment three times now. Send help." -t Loop -s Severe
    # Output: [ANOMALY:Loop|Severe] I've relived this exact moment three times now. Send help.
    ```

3.  **A critical spacetime shift:**
    ```bash
    nightly-temporal-anomaly-tagger -d "The entire building just swapped places with a medieval castle for 30 seconds." -t Shift -s Critical
    # Output: [ANOMALY:Shift|Critical] The entire building just swapped places with a medieval castle for 30 seconds.
    ```

## Development

### Running Tests

To run the integrated unit tests:

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
    └── test_main.rs
```
