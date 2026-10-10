# nightly-forest-fire-simulator

Simulate a forest‑fire cellular automaton in the terminal.

## Usage

```sh
cargo run --release -- <width> <height> <steps> <tree_density> <lightning_prob>
```

- **width**, **height** – dimensions of the grid (e.g., `20 10`).
- **steps** – how many simulation steps to display.
- **tree_density** – float `0.0‑1.0` probability that a cell starts as a tree.
- **lightning_prob** – float `0.0‑1.0` probability that a tree ignites spontaneously each step.

The grid is printed each step using the following symbols:

- `.` – empty ground
- `🌲` – tree
- `🔥` – burning tree

## Example

```sh
cargo run -- 30 15 10 0.6 0.001
```

This creates a 30×15 forest with 60 % tree coverage and runs 10 steps, with a tiny chance of spontaneous ignition.

## Testing

Run the test suite with:

```sh
cargo test
```

The tests are deterministic and do not require external resources.
