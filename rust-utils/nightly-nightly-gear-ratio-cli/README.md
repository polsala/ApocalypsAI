# Nightly Gear Ratio CLI

Calculate bicycle gear inches from chainring, cog, and wheel diameter.

## Usage

```sh
cargo run -- <CHAINRING> <COG> [WHEEL_DIAMETER_MM]
```

- `<CHAINRING>`: Number of teeth on the chainring (e.g., 50)
- `<COG>`: Number of teeth on the rear cog (e.g., 12)
- `[WHEEL_DIAMETER_MM]` (optional): Wheel diameter in millimetres; defaults to **700** mm if omitted.

### Example

```sh
cargo run -- 50 12
```

Output:
```
Gear inches: 84.30
```

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
