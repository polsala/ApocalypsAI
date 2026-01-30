# Nightly Battery Prognosticator

A whimsical CLI tool that estimates how many hours of power remain in your device, factoring in a "radiation" multiplier for post‑apocalyptic flair.

## Installation

```sh
cargo build --release
```

The binary will be at `target/release/nightly-battery-prognosticator`.

## Usage

```sh
nightly-battery-prognosticator <current_percent> <consumption_per_hour> [radiation_factor]
```

- `current_percent`: current battery charge (0‑100)
- `consumption_per_hour`: average percent drained per hour
- `radiation_factor` (optional): multiplier to simulate radiation‑induced drain (default 1.0)

### Example

```sh
nightly-battery-prognosticator 75 5 1.2
```

Output:

```
Estimated remaining hours: 18.00
```

## Tests

Run the test suite with:

```sh
cargo test
```
