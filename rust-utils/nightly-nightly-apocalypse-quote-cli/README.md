# Nightly Apocalypse Quote CLI

A tiny Rust command‑line tool that prints a random apocalypse‑themed quote. Perfect for a quick dose of drama while you code.

## Usage

```sh
cargo run --quiet
```

Will print a random quote.

You can also specify a seed to get a deterministic quote (useful for testing):

```sh
cargo run --quiet -- --seed 2
```

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
