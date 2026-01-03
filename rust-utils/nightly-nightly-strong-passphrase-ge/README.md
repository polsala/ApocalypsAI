# nightly-strong-passphrase-generator

A whimsical yet useful CLI that generates deterministic strong passphrases with optional numbers and symbols.

## Usage

```bash
cargo run -- --words 4 --include-numbers --include-symbols
```

### Options

- `--words N` – number of words in the passphrase (default 4)
- `--include-numbers` – append a 3‑digit number
- `--include-symbols` – append a random symbol from `!@#$%^&*`

The passphrase is deterministic if the environment variable `PASSGEN_SEED` is set, which is useful for testing.

## Example

```bash
$ PASSGEN_SEED=42 cargo run
date-kiwi-honeydew-elderberry
```

## Tests

Run `cargo test` to execute the deterministic unit tests.
```
