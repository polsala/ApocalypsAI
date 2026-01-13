# Scavenger Map Generator

`nightly-scavenger-map-generator` is a tiny Rust commandâline tool that spits out an ASCII map of a postâapocalyptic landscape filled with resources you specify.  Itâs perfect for tabletop RPGs, improv storytelling, or just for fun.

## Installation

```sh
# Clone the repository (or copy the generated folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd rust-utils/nightly-scavenger-map-generator

# Build and install locally
cargo install --path .
```

## Usage

```sh
scavenger-map \
    --width 20 \
    --height 10 \
    --resources water,food,ammo,medicine \
    --seed 42
```

* `--width` and `--height` define the size of the map.
* `--resources` is a commaâseparated list; the first letter of each resource is used as the map symbol (e.g., `water` â `W`).
* `--seed` makes the placement deterministic â useful for testing or sharing the same map with friends.

The output looks like this (example with the arguments above):

````
....................
..W...........A.....
......F.............
...........M........
....................
......A.............
....................
..F.................
....................
........W...........
````

## How It Works

1. The program parses the commandâline arguments.
2. It creates a `StdRng` seeded with the provided `--seed` (or a random seed if omitted).
3. For each resource it picks a random empty cell and places the resourceâs capitalised first letter there.
4. All remaining cells are filled with `.` (dot).
5. The final grid is printed to STDOUT.

## Testing

Run the test suite with:

```sh
cargo test
```

The tests verify deterministic placement, correct dimensions, and that each resource appears exactly once.

## License

MIT â see the LICENSE file in the repository root.
