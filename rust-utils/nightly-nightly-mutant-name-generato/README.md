# Mutant Name Generator

A tiny Rust CLI that creates a random, post‑apocalyptic mutant name.

## Usage

```sh
cargo run --quiet -- [--seed <u64>]
```

- `--seed` optional integer to make the output deterministic.

## Example

```sh
$ cargo run --quiet -- --seed 42
Feral Reaper
```

## Building

```sh
cargo build --release
```

## Testing

```sh
cargo test
```
