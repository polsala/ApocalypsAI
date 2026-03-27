# nightly-radiation-estimator

Estimates cumulative radiation exposure for survivors in a post‑apocalyptic setting.

## Usage

```sh
cargo run -- --hours 3.5 --level 4
```

The program prints the total dose in Sieverts (Sv) and warns if the dose exceeds a safe threshold (10 Sv).

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
