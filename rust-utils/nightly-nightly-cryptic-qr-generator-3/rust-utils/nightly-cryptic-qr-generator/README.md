# Cryptic QR Generator

A whimsical Rust CLI that turns any text into an ASCII “QR code”. It simply reverses the input and wraps it in a box, making it easy to share short strings in terminal chats, logs, or post‑apocalyptic notes.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
cryptic-qr "Hello world"
```

Output:

```
+------+
| dlrow olleH |
+------+
```

## How it works

The tool reverses the input string and formats it as:

```
+------+
| <reversed> |
+------+
```

## License

MIT
