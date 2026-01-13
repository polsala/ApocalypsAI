# Nightly Chrono Converter

A tiny Rust CLI that converts between humanâreadable duration strings (e.g., `1d2h3m4s`) and total seconds.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
# Convert to seconds
chrono-converter --to-seconds "1d2h3m4s"
# => 93784

# Convert from seconds
chrono-converter --from-seconds 93784
# => 1d2h3m4s
```

## Supported units

- `d` â days (24â¯h)
- `h` â hours
- `m` â minutes
- `s` â seconds

Units may appear in any order, numbers must be nonânegative integers.

## Testing

```sh
cargo test
```
