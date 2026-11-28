# nightly‑radiation‑decay‑cli

A tiny Rust command‑line utility that calculates the remaining radiation dose after a certain elapsed time, based on the half‑life decay model.

## Installation

```bash
# From the repository root
cd rust-utils/nightly-radiation-decay-cli
cargo build --release
```

The binary will be located at `target/release/radiation-decay-cli`.

## Usage

```bash
radiation-decay-cli --initial <mSv> --half-life <hours> --elapsed <hours>
```

- `--initial` (`-i`): Initial radiation dose in millisieverts (mSv).
- `--half-life` (`-h`): Half‑life of the radioactive material in hours.
- `--elapsed` (`-e`): Time elapsed since the initial measurement, in hours.

The program prints the remaining dose rounded to three decimal places.

### Example

```bash
$ radiation-decay-cli -i 100 -h 10 -e 15
31.250 mSv remaining
```

The calculation follows:

```
remaining = initial * 0.5^(elapsed / half_life)
```

## Testing

Run the test suite with:

```bash
cargo test
```

All tests are deterministic and run offline.
