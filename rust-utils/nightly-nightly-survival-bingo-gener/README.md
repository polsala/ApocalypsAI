nightly-survival-bingo-generator

Generate a 5x5 survival bingo card with unique tasks.

Usage

cargo run --release

or build the binary:

cargo build --release
./target/release/nightly-survival-bingo-generator

The program prints a bingo card to stdout. Each column is labeled A–E.

Reproducibility

Set the BINGO_SEED environment variable to a 64‑bit integer to get a deterministic card:

export BINGO_SEED=123456
cargo run

Example Output

A: Find water
B: Build shelter
C: Gather firewood
D: Cook food
E: Signal for help
...
