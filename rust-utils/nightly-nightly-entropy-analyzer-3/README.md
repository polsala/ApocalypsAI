# nightly-entropy-analyzer

Compute the Shannon entropy of an input string. Useful for quickly estimating the strength of passwords or random data.

## Usage

```sh
cargo run -- <string>
```

Example:

```sh
cargo run -- "password123"
Entropy: 3.180832 bits per character
```

The program prints the entropy in bits per character with six decimal places.

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
