Rusty Fortune Cookie

A whimsical CLI that prints a deterministic fortune based on the current date or a provided seed. Useful for daily motivation or as a fun terminal decoration.

Usage:
  cargo run -- --seed 42
  cargo run -- --date 2023-01-01

If no arguments are given, it uses the current UTC date.

Example output:
  Your fortune: The early bird catches the worm.

Installation:
  cargo install --path .

Testing:
  cargo test
