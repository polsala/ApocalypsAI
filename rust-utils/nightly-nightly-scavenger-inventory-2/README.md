# Nightly Scavenger Inventory Generator

A whimsical Rust CLI that creates a random post‑apocalyptic scavenger inventory list.

## Usage

```sh
cargo run --quiet
# or with a fixed seed for reproducible output
SCAV_SEED=42 cargo run --quiet
```

The program prints five items with quantities, e.g.:

```
3 x Canned Beans
1 x Rusty Pipe
5 x Solar Charger
2 x Mutant Mushroom
4 x Tattered Map
```

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
