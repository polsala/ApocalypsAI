# nightly-battery-estimator

Estimates remaining battery life based on current charge and average consumption rate. Includes a whimsical "survival mode" that simulates radiation‑induced power drain.

## Usage

```sh
cargo run -- <charge_percent> <consumption_rate_per_hour> [--survival]
```

- `<charge_percent>`: current battery charge (0‑100)
- `<consumption_rate_per_hour>`: percent drained per hour (e.g., 5)
- `--survival`: increase drain by 25% to account for post‑apocalyptic conditions.

The program prints estimated remaining hours.

## Example

```sh
$ cargo run -- 80 4
Estimated remaining time: 20.00 hours
```

With survival mode:

```sh
$ cargo run -- 80 4 --survival
Estimated remaining time (survival mode): 16.00 hours
```

## Tests

Run `cargo test` to execute deterministic unit tests.
