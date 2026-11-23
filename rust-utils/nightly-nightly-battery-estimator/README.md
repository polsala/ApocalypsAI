# Nightly Battery Life Estimator

A whimsical CLI tool that estimates how many hours of power you have left in a post‑apocalyptic setting.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
battery-estimator <current_percent> <consumption_per_hour>
```

Example:

```sh
battery-estimator 57 12.5
```

The program will print the estimated hours left and a fun, themed message.

## License

MIT
