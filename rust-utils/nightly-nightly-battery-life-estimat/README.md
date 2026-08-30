# Battery Life Estimator

A whimsical CLI tool for post‑apocalyptic survivors to estimate how many hours their device will survive on the remaining battery.

## Usage

```sh
battery-life-estimator <capacity_mAh> <draw_mA> [efficiency]
```

- `capacity_mAh`: current battery capacity in milliamp‑hours.
- `draw_mA`: average current draw in milliamps.
- `efficiency` (optional): efficiency factor (0.0‑1.0), default `0.9`.

### Example

```sh
battery-life-estimator 2500 500
# => Estimated remaining time: 4.50 hours
```

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
