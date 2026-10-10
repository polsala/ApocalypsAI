# Nightly Survival Kit Builder

A tiny Rust CLI that prints a ready‑made survival kit checklist for a given post‑apocalyptic scenario.

## Usage

```sh
cargo run -- <scenario>
```

Supported scenarios: `zombie`, `radiation`, `flood`. Any other value falls back to a generic kit.

## Example

```sh
$ cargo run -- zombie
- Baseball bat
- Spare ammo
- First aid kit
- Water filter
```

## Testing

```sh
cargo test
```
