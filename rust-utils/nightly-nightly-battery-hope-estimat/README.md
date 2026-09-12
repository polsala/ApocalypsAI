# Battery Hope Estimator

A tiny Rust CLI that estimates how many hours of power remain given current capacity and average draw, and adds a whimsical apocalypse‑themed message.

## Usage

```sh
battery-hope-estimator <capacity_mAh> <draw_mA> [efficiency]
```

- `capacity_mAh`: current battery capacity in milliamp‑hours.
- `draw_mA`: average current draw in milliamps.
- `efficiency` (optional, default 0.9): efficiency factor (0‑1).

Example:

```sh
battery-hope-estimator 4000 500
```

Outputs:

```
Estimated remaining time: 7.20 hours.
Stay powered, survivor!
```

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
