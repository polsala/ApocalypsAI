# nightly-entropy-seed

Generate a random string of configurable length and alphabet.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
entropy-seed -l 16          # 16‑character random string (default alphanumeric)
entropy-seed -l 32 -a "ABC" # 32 chars using only A, B, C
```

## Options

- `-l, --length <LEN>`: Length of output (default 16)
- `-a, --alphabet <ALPH>`: Characters to draw from (default alphanumeric)

## Deterministic mode (for testing)

Set the `ENTROPY_SEED` environment variable to a numeric seed to get reproducible output.

```sh
ENTROPY_SEED=42 entropy-seed -l 8
```
