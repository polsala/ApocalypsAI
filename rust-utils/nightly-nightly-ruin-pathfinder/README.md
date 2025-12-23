# Nightly Ruin Pathfinder

A tiny Rust CLI that reads a rectangular map of a ruined city and finds the shortest path from `S` (start) to `E` (end) avoiding obstacles (`#`). It prints the map with the path marked by `*`.

## Usage

```sh
cargo run --release -- path/to/map.txt
```

If no file is given, the program reads from **stdin**.

## Map format
- `.` – open space
- `#` – obstacle / wall
- `S` – start position (exactly one)
- `E` – end position (exactly one)

All rows must be the same length.

## Example

**Input (`map.txt`)**
```
S..#
.##.
...E
```

**Output**
```
S**#
.*#.
..*E
```

## Building & Testing

```sh
# Build the binary
cargo build --release

# Run the tests
cargo test
```

Enjoy navigating the wastelands!
