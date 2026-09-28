# nightly-battery-life-estimator

Estimate how long a battery will last given its capacity (mAh) and device draw (mA).

## Usage

```sh
nightly-battery-life-estimator <capacity_mAh> <draw_mA>
```

- `<capacity_mAh>`: Battery capacity in milliamp-hours.
- `<draw_mA>`: Device power draw in milliamps.

The tool prints the estimated runtime in hours (rounded to two decimal places). If the draw is `0`, it reports infinite runtime.

## Example

```sh
$ nightly-battery-life-estimator 2000 500
4.00 hours
```

## Building

```sh
cargo build --release
```

The binary will be located at `target/release/nightly-battery-life-estimator`.
