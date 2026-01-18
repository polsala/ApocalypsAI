# nightly-radiation-decay-cli

A whimsical yet practical command‑line tool that estimates remaining radiation after a given time using exponential decay (half‑life). Perfect for post‑apocalypse role‑playing games or quick scientific calculations.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
radiation_decay --initial 1000 --half-life 30 --time 45
```

Outputs the remaining radiation level.

## Parameters

- `--initial`: initial radiation level (any units)
- `--half-life`: half‑life period (same time units as `--time`)
- `--time`: elapsed time

## Example

```
$ radiation_decay -i 800 -l 20 -t 40
Remaining radiation: 200.0
```

## Testing

Run `cargo test` to execute the deterministic unit tests.
