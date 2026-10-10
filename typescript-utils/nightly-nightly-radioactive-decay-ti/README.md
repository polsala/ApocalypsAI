# Nightly Radioactive Decay Timer

Utility to calculate the remaining quantity of a radioactive substance after a given elapsed time using its half‑life.

## Installation

```sh
npm install -g nightly-radioactive-decay-timer
```

## Usage

```sh
nrdt --initial 100 --half-life 30 --time 90
# Output: Remaining amount: 12.5
```

## Options

- `--initial <number>`: Initial amount (default `1`).
- `--half-life <number>`: Half‑life period (must be positive, same units as `--time`).
- `--time <number>`: Elapsed time.

The tool prints the remaining amount to stdout. Errors are printed to stderr and cause a non‑zero exit code.

## License

MIT
