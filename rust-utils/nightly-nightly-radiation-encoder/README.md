# Nightly Radiation Encoder

A whimsical CLI tool that encodes a secret message into a "radiation‑resistant" base‑36 string with a simple checksum, and can decode it back. Useful for fun secret notes in post‑apocalyptic role‑play.

## Installation

```sh
cargo build --release
```

The binary will be at `target/release/radiation-encoder`.

## Usage

### Encode a message

```sh
./radiation-encoder encode "Stay safe, wanderer"
```

Output (example):

```
1s6a6c6e6f6c6d6e6f6g6h9
```

### Decode a message

```sh
./radiation-encoder decode 1s6a6c6e6f6c6d6e6f6g6h9
```

Output:

```
Stay safe, wanderer
```

## How it works

- Each byte of the UTF‑8 input is split into two 4‑bit nibbles.
- Each nibble is represented as a base‑36 digit (0‑9, a‑z). For values 0‑15 this yields `0‑9` and `a‑f`.
- A checksum character is appended, calculated as the sum of the original bytes modulo 36.
- Decoding verifies the checksum and reconstructs the original bytes.

## License

MIT
