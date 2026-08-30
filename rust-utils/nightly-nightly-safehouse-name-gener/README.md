# nightly-safehouse-name-generator

Generates whimsical post‑apocalyptic safe‑house names.

## Usage

```sh
cargo run --quiet -- [--seed <NUMBER>]
```

- `--seed` optional 64‑bit integer to make the output deterministic.

## Example

```sh
$ cargo run --quiet -- --seed 42
Radiant Oasis
```

## Building

```sh
cargo build --release
```

## Testing

```sh
cargo test
```
