# nightly-battery-life-estimator

Estimate how long a battery will last given its capacity and device consumption.

## Usage

```sh
battery-life <capacity_mAh> <consumption_mA>
```

Example:

```sh
battery-life 5000 250
# Output: Estimated runtime: 20.00 hours
```

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
