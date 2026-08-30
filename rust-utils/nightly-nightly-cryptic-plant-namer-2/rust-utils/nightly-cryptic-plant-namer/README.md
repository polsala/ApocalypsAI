# Cryptic Plant Namer

A tiny Rust CLI that conjures whimsical, Latin‑flavored plant names. Perfect for writers, game masters, or anyone who needs a touch of botanical mystery.

## Usage

```sh
cargo run --quiet
```

Each execution prints a random plant name, e.g.:

```
Radiant petalus
```

You can also use the library directly:

```rust
use cryptic_plant_namer::generate_name;
let name = generate_name(0, 2); // "Gleaming petalus"
```

## How it works

The tool picks an adjective from a short list and combines it with a Latin‑style suffix. The `generate_name` function is deterministic given indices, making it easy to test.

## Testing

```sh
cargo test
```
