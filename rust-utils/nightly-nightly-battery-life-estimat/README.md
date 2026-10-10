# Battery Life Estimator

A whimsical CLI tool to estimate remaining battery life in hours based on current capacity, average draw, and an optional efficiency factor.

## Build

```sh
cargo build --release
```

## Usage

```sh
battery-life-estimator <capacity_mAh> <draw_mA> [efficiency]
```

- `capacity_mAh`: current battery capacity in mAh.
- `draw_mA`: average power draw in mA.
- `efficiency` (optional): efficiency factor (0.0‑1.0), default **0.9**.

### Example

```sh
$ battery-life-estimator 3000 500
Estimated battery life: 5.40 hours
```

## Testing

```sh
cargo test
```
