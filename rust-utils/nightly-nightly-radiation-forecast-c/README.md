# nightly-radiation-forecast-cli

Estimates fictional radiation levels for given latitude and longitude using a whimsical deterministic algorithm.

## Usage

```sh
cargo run -- <latitude> <longitude>
```

Example:

```sh
cargo run -- 34.05 -118.25
Radiation level at (34.05, -118.25): 57 mSv
```

## Build

```sh
cargo build --release
```

## How it works

The tool computes a pseudo‑random radiation level between 1 and 100 mSv based on the absolute values of the coordinates:

```
level = ((|lat| * 31 + |lon| * 17) % 100) + 1
```
