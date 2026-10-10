# Nightly Temporal Echo Tuner

## Overview

The `nightly-temporal-echo-tuner` is a whimsical-yet-useful CLI tool designed to detect subtle 'temporal echoes' – minor distortions in the fabric of reality – and offer personalized, harmonizing suggestions. Whether you're feeling a slight temporal drift or just need a moment of existential re-alignment, this tuner is here to help you find your temporal resonance frequency.

Built with Rust for blazing-fast echo detection and robust reality-tuning capabilities.

## Features

*   **Temporal Echo Detection**: Generates a unique 'resonance frequency' based on a provided seed or the current timestamp.
*   **Whimsical Harmonizing Suggestions**: Offers a lighthearted, actionable suggestion to help re-align your personal temporal flow.
*   **Deterministic Output**: With a provided seed, the output (frequency and suggestion) is entirely predictable, making it great for consistent reality checks.
*   **Lightweight & Fast**: A high-performance CLI tool written in Rust.

## Installation

To install `nightly-temporal-echo-tuner`, you'll need Rust and Cargo installed on your system. If you don't have them, you can install them via `rustup`:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

Once Rust is set up, clone this repository and build the utility:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-temporal-echo-tuner
cargo install --path .
```

This will install the `nightly-temporal-echo-tuner` binary to your Cargo bin directory (usually `~/.cargo/bin`), making it available globally.

## Usage

Run the tuner from your terminal:

```bash
nightly-temporal-echo-tuner
```

Example Output:

```
Temporal Echo Detected!
  Resonance Frequency: 512.73 Hz
  Harmonizing Suggestion: Contemplate the true nature of toast. Is it bread, or something more?

Stay vigilant, fellow temporal traveler!
```

### Options

*   **`-s, --seed <STRING>`**: Provide a custom string to seed the temporal echo detection. This ensures deterministic output.

    ```bash
    nightly-temporal-echo-tuner --seed "my-lucky-day"
    ```

*   **`-f, --frequency-only`**: Output only the raw temporal resonance frequency.

    ```bash
    nightly-temporal-echo-tuner --seed "my-lucky-day" --frequency-only
    ```

    Example Output:

    ```
    104.28 Hz
    ```

## Development

To build and run from source:

```bash
cd ApocalypsAI/rust-utils/nightly-temporal-echo-tuner
cargo run
```

To run with a specific seed:

```bash
cargo run -- --seed "dev-test-seed"
```

## Testing

Run the automated tests to ensure the tuner is functioning correctly:

```bash
cd ApocalypsAI/rust-utils/nightly-temporal-echo-tuner
cargo test
```

Tests are deterministic and offline, using fixed seeds to ensure consistent output for verification.
