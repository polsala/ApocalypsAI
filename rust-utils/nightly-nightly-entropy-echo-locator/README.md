# Nightly Entropy Echo Locator

## Summary

The `nightly-entropy-echo-locator` is a high-performance command-line utility crafted in Rust. It calculates the Shannon entropy of specified files, providing a numerical measure of their randomness or 'signal clarity'. In a post-apocalyptic data landscape, high entropy might indicate encrypted messages, compressed archives, or truly random data – potential 'signals' amidst the noise.

## Usage

```bash
nightly-entropy-echo-locator <FILE_PATH> [FILE_PATH...]
```

### Arguments

*   `<FILE_PATH>`: One or more paths to files whose entropy you wish to calculate.

### Examples

Calculate entropy for a single file:

```bash
nightly-entropy-echo-locator data/secret_transmission.bin
```

Calculate entropy for multiple files:

```bash
nightly-entropy-echo-locator logs/system.log config/settings.toml
```

Expected output format:

```
File: data/secret_transmission.bin, Entropy: 7.987 bits/byte
File: logs/system.log, Entropy: 4.521 bits/byte
```

## Installation

To build and install from source, ensure you have Rust and Cargo installed.

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-entropy-echo-locator
cargo build --release
./target/release/nightly-entropy-echo-locator <FILE_PATH>
```

Or, to install globally:

```bash
cargo install --path .
nightly-entropy-echo-locator <FILE_PATH>
```

## How it Works

The tool reads the input file byte by byte, counts the occurrences of each possible byte value (0-255), and then applies the Shannon entropy formula:

`H = - Σ (p_i * log₂(p_i))`

Where `p_i` is the probability of byte `i` occurring. A perfectly random byte stream will approach an entropy of 8 bits/byte, while a highly repetitive or empty file will have an entropy close to 0.
