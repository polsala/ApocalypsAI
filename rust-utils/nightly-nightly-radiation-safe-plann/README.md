# Nightly Radiation Safe Planner

A whimsical CLI tool for post‑apocalypse wanderers. Given a maximum safe radiation level and a list of locations with their radiation readings, it prints the names of locations that are safe to visit.

## Installation

```sh
cargo build --release
```

The binary will be located at `target/release/radiation_safe`.

## Usage

```sh
# Provide a max safe radiation level as the sole argument
# Pipe a list of "Location:Radiation" lines into the program

echo -e "Vault:12\nWasteland:85\nOasis:30" | ./target/release/radiation_safe 40
```

**Output**

```
Vault
Oasis
```

## How it works

The program reads lines from *stdin* in the format `Location:Radiation`. It filters out any location whose radiation exceeds the provided threshold and prints the safe location names, one per line.

## Testing

Run the test suite with:

```sh
cargo test
```

The tests cover basic filtering, handling of malformed lines, and edge cases.
