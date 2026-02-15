# nightly-epoch-converter-rs

A blazing‑fast Rust command‑line utility that converts between ISO‑8601 timestamps and Unix epoch seconds.

## Build

```sh
cargo build --release
```

## Usage

```sh
# Convert ISO‑8601 to epoch
nightly-epoch-converter-rs --to-epoch 2023-10-31T12:00:00Z
# => 1698744000

# Convert epoch to ISO‑8601
nightly-epoch-converter-rs --from-epoch 1698744000
# => 2023-10-31T12:00:00+00:00
```

The tool validates input and prints an error message on failure.

## License

MIT
