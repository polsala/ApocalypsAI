# Battery Hope Estimator

A whimsical CLI tool for post‑apocalypse survivors to estimate how many hours of power remain in their batteries.

## Installation

```sh
cargo build --release
```

The binary will be located at `target/release/battery-hope`.

## Usage

```sh
battery-hope <used_hours> <avg_consumption_watts> <battery_capacity_wh>
```

**Example**

```sh
battery-hope 5 12 100
```

The program will output the estimated remaining hours and a morale‑boosting message.

## How it works

It assumes linear consumption:

```
remaining = (capacity / avg_consumption) - used_hours
```

If the calculation yields a negative value, it is clamped to zero. A consumption of zero yields an infinite estimate.

## Testing

```sh
cargo test
```

All tests run offline and are deterministic.
