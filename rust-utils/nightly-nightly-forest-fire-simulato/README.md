# nightly-forest-fire-simulator

A whimsical command‑line tool that visualises a simple forest‑fire cellular automaton. Useful for teaching basic simulation concepts or just watching trees burn in ASCII art.

## Build

```sh
cargo build --release
```

## Usage

```sh
./target/release/forest-fire-simulator --width 30 --height 10 --steps 20 --seed 42
```

* `--width`  : number of columns (default 30)
* `--height` : number of rows (default 15)
* `--steps`  : how many generations to simulate (default 100)
* `--seed`   : optional RNG seed for reproducible runs. If omitted, the current system time is used.

## How it works

Each cell can be one of three states:

* **Empty**   – nothing there (` `)
* **Tree**    – a healthy tree (`🌲`)
* **Burning** – a tree on fire (`🔥`)

The simulation follows the classic forest‑fire rules:

1. A **Burning** cell becomes **Empty** in the next step.
2. A **Tree** becomes **Burning** if at least one of its eight neighbours is **Burning**.
3. Independently, a **Tree** can spontaneously ignite with a tiny probability (0.001) – this randomness is driven by the provided seed.

The grid is printed to the terminal after each step, giving a live‑view of the blaze.

## License

MIT
