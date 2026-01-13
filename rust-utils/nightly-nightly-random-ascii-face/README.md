# nightly-random-ascii-face

Generate a random ASCII face with optional style and seed.

## Usage

```bash
cargo run -- --seed 42 --style smile
```

Options:

- `--seed <u64>`: Optional seed for deterministic output.
- `--style <style>`: Optional style filter (`smile`, `frown`, `surprised`).

## Examples

```bash
# Random face
cargo run -- --seed 42
# Smile face
cargo run -- --style smile
# Deterministic smile
cargo run -- --seed 42 --style smile
```

## Tests

Run `cargo test` to execute the test suite.
