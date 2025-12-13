# nightly-emoji-hex-encoder

Encode and decode text to a whimsical emoji‑hex representation via a fast Rust CLI.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
# Encode
nightly-emoji-hex-encoder encode "Hello"

# Decode
nightly-emoji-hex-encoder decode "😃😁..."
```

## How it works

Each byte is split into two 4‑bit nibbles. Each nibble is mapped to one of 16 emojis:

0 → 😀
1 → 😁
2 → 😂
3 → 🤣
4 → 😃
5 → 😄
6 → 😅
7 → 😆
8 → 😉
9 → 😊
A → 😋
B → 😎
C → 😍
D → 😘
E → 🥰
F → 🤩

## License

MIT
