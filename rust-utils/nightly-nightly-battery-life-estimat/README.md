# Battery Life Estimator

A whimsical CLI tool for the post‑apocalyptic wanderer to estimate how many hours of power remain on a device.

## Build

```sh
cargo build --release
```

## Usage

```sh
./target/release/battery-life-estimator <current_mAh> <consumption_mA>
```

Example:

```sh
./battery-life-estimator 5000 250
# => Estimated remaining time: 20.00 hours
```

If the consumption is `0`, the tool reports "infinite".

## Tests

```sh
cargo test
```
