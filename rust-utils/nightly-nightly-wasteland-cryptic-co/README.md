# Nightly Wasteland Cryptic Compass

A tiny Rust CLI that spits out a cryptic, post‑apocalyptic navigation hint based on a cardinal direction (N, E, S, W) and an optional numeric seed. Perfect for role‑playing games, story prompts, or just adding a bit of mystery to your terminal.

## Build

```bash
# Ensure you have Rust toolchain installed (rustc + cargo)
cargo build --release
```

The binary will be placed at `target/release/nightly-wasteland-cryptic-compass`.

## Usage

```bash
# Basic usage – random seed based on current time
nightly-wasteland-cryptic-compass N

# Provide an explicit seed for reproducible hints
nightly-wasteland-cryptic-compass E 42
```

### Arguments

- `DIRECTION` – One of `N`, `E`, `S`, `W` (case‑insensitive).
- `SEED` – Optional unsigned integer. If omitted, the program uses the current Unix timestamp as the seed.

## Example Output

```text
> nightly-wasteland-cryptic-compass S 7
Follow the rusted compass toward the howling dunes, where shadows whisper.
```

## License

MIT – see the LICENSE file in the repository.
