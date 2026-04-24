# nightly-battery-forecast

Estimates remaining battery life and gives apocalypse‑themed warnings.

## Usage

```sh
battery-forecast <current_percent> <consumption_rate_mAh_per_hour> <battery_capacity_mAh>
```

Example:

```sh
battery-forecast 45 1500 6000
```

The tool will print the estimated hours left and a whimsical warning.

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
