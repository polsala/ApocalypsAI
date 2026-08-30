# nightly-radiation-exposure-calculator

Estimate the maximum safe exposure time to radiation given a constant radiation level and a dose limit.

## Usage

```sh
cargo run --quiet -- <radiation_uSv_per_h> <dose_limit_mSv>
```

Example:

```sh
cargo run --quiet -- 250 0.5
```

Outputs:

```
2.00
```

## Building without Cargo

If you prefer to compile directly with `rustc`:

```sh
rustc src/main.rs -o radiation_calc
./radiation_calc 250 0.5
```

## Testing

```sh
cargo test
```

The test suite verifies the core calculation logic and the CLI output.
