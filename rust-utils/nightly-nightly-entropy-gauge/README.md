# nightly-entropy-gauge

Utility to compute the Shannon entropy of a file or standard input. Useful for assessing randomness, detecting compressed or encrypted data, and just for fun in the apocalypse.

## Installation

```bash
# Build and install locally
cargo install --path .
```

Or compile manually:

```bash
cargo build --release
./target/release/entropy-gauge <path>
```

## Usage

```bash
# Compute entropy of a file
entropy-gauge path/to/file.bin

# Compute entropy from stdin (use "-" or omit argument)
cat file.bin | entropy-gauge -
```

The program prints the entropy in **bits per byte** with six decimal places.

## Examples

```bash
$ echo -n "aaaa" | entropy-gauge -
0.000000
$ echo -n "abcd" | entropy-gauge -
2.000000
```

## How it works

The tool reads the entire input, counts the frequency of each byte (0‑255), and applies the Shannon entropy formula:

```
H = - Σ p_i * log2(p_i)
```

where *p_i* is the probability of byte *i*.

## License

MIT © ApocalypsAI
