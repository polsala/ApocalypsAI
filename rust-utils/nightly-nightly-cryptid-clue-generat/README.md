# Cryptid Clue Generator

A whimsical Rust CLI that generates a random post‑apocalyptic cryptid sighting clue. Useful for tabletop RPGs, writing prompts, or just fun.

## Build

```sh
cargo build --release
```

## Usage

```sh
cargo run -- [SEED]
```

*Optional* `SEED` (a `u64`) makes the output deterministic.

### Example

```sh
$ cargo run -- 42
A haunting Chupacabra spotted near the flooded subway.
```

## Testing

```sh
cargo test
```
