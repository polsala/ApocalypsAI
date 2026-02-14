# Cryptic Plant Namer

A whimsical CLI tool that generates mysterious plant names for world‑building, games, or creative writing.

## Installation

```sh
cargo build --release
```

The binary will be at `target/release/cryptic-plant-namer`.

## Usage

```sh
# Random name (uses current timestamp as seed)
./cryptic-plant-namer

# Deterministic name with a seed (useful for tests)
./cryptic-plant-namer --seed 42
```

## How it works

Combines a random adjective with a Latin‑sounding root and appends “ia”.

## License

MIT
