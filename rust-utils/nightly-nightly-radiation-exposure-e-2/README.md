# Nightly Radiation Exposure Estimator

A whimsical CLI tool that helps post‑apocalyptic survivors estimate how many hours they can stay exposed to a given radiation level before reaching a safe dose limit.

## Usage

```sh
radiation-estimator <level> [limit]
```

- `<level>`: Radiation level in µSv/h (micro‑sieverts per hour). Must be a positive number.
- `[limit]` (optional): Desired dose limit in µSv. Defaults to 1000 µSv.

The program prints the maximum safe exposure time in hours (rounded to two decimals).

## Example

```sh
$ radiation-estimator 250
You can stay exposed for up to 4.00 hours before reaching 1000 µSv.
```

## Building

```sh
cargo build --release
```

## Testing

```sh
cargo test
```
