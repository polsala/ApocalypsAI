# Nightly Void Whisper Classifier

A high-performance CLI tool written in Rust to classify cryptic "void whispers" into predefined categories and assign an urgency level. This utility helps agents quickly triage incoming, often ambiguous, signals from the chaotic environment.

## Features

*   **Categorization**: Classifies whispers into "Resource Alert", "Temporal Anomaly", "Social Chatter", "Existential Dread", or "Unknown".
*   **Urgency Assessment**: Assigns "Low", "Medium", or "High" urgency based on keywords.
*   **Fast & Efficient**: Built with Rust for blazing-fast execution.
*   **Self-contained**: No external runtime dependencies beyond Rust itself.

## Installation

To build and install the `nightly-void-whisper-classif` utility, you need to have Rust and Cargo installed. If you don't have them, follow the instructions on [rust-lang.org](https://www.rust-lang.org/tools/install).

1.  Navigate to the utility's directory:
    ```bash
    cd rust-utils/nightly-void-whisper-classif
    ```
2.  Build the project:
    ```bash
    cargo build --release
    ```
    This will create an executable at `target/release/nightly-void-whisper-classif`.
3.  (Optional) Move the executable to a directory in your PATH for easier access:
    ```bash
    sudo mv target/release/nightly-void-whisper-classif /usr/local/bin/
    ```

## Usage

Run the classifier from your terminal, providing the whisper as a command-line argument:

```bash
nightly-void-whisper-classif --whisper "Danger! Food supplies are critical!"
```

**Example Output:**

```
Whisper: "Danger! Food supplies are critical!"
Classification: Resource Alert
Urgency: High
```

**More Examples:**

*   **Temporal Anomaly (Medium Urgency):**
    ```bash
    nightly-void-whisper-classif --whisper "A temporal rift detected, warning of echoes soon."
    ```
*   **Social Chatter (Low Urgency):**
    ```bash
    nightly-void-whisper-classif --whisper "Hello friend, just a casual message."
    ```
*   **Existential Dread (Low Urgency):**
    ```bash
    nightly-void-whisper-classif --whisper "The void calls, all is meaningless."
    ```
*   **Unknown (Low Urgency):**
    ```bash
    nightly-void-whisper-classif --whisper "Just some random noise in the static."
    ```

## Development & Testing

To run the tests:

```bash
cd rust-utils/nightly-void-whisper-classif
cargo test
```
