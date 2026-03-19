# Battery Life Estimator

A whimsical CLI tool for post‑apocalypse survivors to estimate how many hours their device will survive on the remaining battery.

## Build

```sh
cargo build --release
```

## Usage

```sh
nightly-battery-life-estimator <capacity_mAh> <consumption_mA>
```

Example:

```sh
nightly-battery-life-estimator 5000 250
# => Estimated remaining time: 20.00 hours
```

## Tests

```sh
cargo test
```
