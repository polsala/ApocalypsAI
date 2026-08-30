# nightly-entropy-aurora

A whimsical Rust CLI that measures the Shannon entropy of a file (or stdin) and visualizes it with a colorful bar and apocalyptic commentary.

## Installation

```sh
# Clone the repository and build
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/rust-utils/nightly-entropy-aurora
cargo build --release
# The binary will be at target/release/entropy-aurora
```

## Usage

```sh
# Measure a file
entropy-aurora path/to/file.txt

# Pipe data from another command
cat file.txt | entropy-aurora
```

The program prints:

* **Entropy** – bits per byte (0‑8).
* **Bar** – a visual representation where `█` is entropy and `░` is emptiness.
* **Commentary** – a short, whimsical message describing the chaos level.

## Example

```sh
$ echo "hello world" | entropy-aurora
Entropy: 3.18 bits/byte
[██████░░░░░░░░░░░░░]
Some randomness, but the void is calm.
```

## License

MIT © ApocalypsAI
