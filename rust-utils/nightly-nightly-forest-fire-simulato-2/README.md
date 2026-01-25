# nightly-forest-fire-simulator

**A whimsical yet educational Rust CLI** that simulates a simple forest‑fire cellular automaton.

## What it does
- The world is a rectangular grid of cells.
- Each cell can be **Tree (🌲)**, **Burning (🔥)**, or **Empty ( )**.
- Rules per step:
  1. A burning cell becomes empty.
  2. A tree catches fire if at least one orthogonal neighbour is burning.
  3. A tree may spontaneously ignite with a tiny probability (default 5%).
- The simulation prints the grid after each step using ASCII/emoji characters.

## Build & Run
```bash
# Clone the repository (or copy the generated folder) and cd into it
cargo build --release

# Run the simulator
#   <width> <height> <steps> [seed]
# Example: a 20×10 grid for 15 steps with a deterministic seed of 42
cargo run --release -- 20 10 15 42
```

If the optional *seed* is omitted, the program uses `0` as the seed, which makes the simulation deterministic for the same dimensions and step count.

## Example Output
```
🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲
🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲
🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲
...
```

## Testing
The project includes deterministic unit tests that verify the automaton logic using a fixed pseudo‑random generator. Run them with:
```bash
cargo test
```

## License
MIT – see the LICENSE file in the repository.
