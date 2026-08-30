# Nightly Wasteland Nickname Generator

A tiny Rust CLI that turns any name into a post‑apocalyptic nickname.

## Usage

```sh
cargo run -- <name>
# or pipe a name via stdin
echo "Bob" | cargo run
```

Example:

```
$ cargo run -- Alice
Ashen Alice the Keeper
```

## How it works

The program computes a simple checksum of the input string, then selects an adjective and a title from predefined lists. The result is deterministic – the same input always yields the same nickname.

## Build & Test

```sh
cargo build --release
cargo test
```
