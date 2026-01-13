# Scavenger Map Generator

A tiny Rust CLI that creates a random ASCII map for postâapocalyptic scavenging games.

## Features

- Random placement of userâdefined resource symbols (e.g., food, water, ammo)
- Adjustable map width and height
- Optional numeric seed for reproducible maps
- Pure ASCII output, easy to copyâpaste into chat or notes

## Installation

```bash
# Clone the repository (or copy the generated folder)
git clone https://github.com/your-org/apocalypsai.git
cd utils/nightly-scavenger-map

# Build the binary
cargo build --release

# The executable will be at target/release/scavenger-map
```

## Usage

```bash
./target/release/scavenger-map <width> <height> <resources> [seed]
```

- **width**, **height**: Positive integers defining the map size.
- **resources**: Commaâseparated list of singleâcharacter symbols representing resources (e.g., `F,W,R` for Food, Water, Radio).
- **seed** (optional): Integer seed for deterministic output. Omit for a random seed.

### Example

```bash
./target/release/scavenger-map 20 10 F,W,R 12345
```

Might produce something like:

```.F...W...........R.
..W......F...R....
....R...W...F.....
...F......R...W...
.W...R...F........
....W...R...F.....
...R......W...F...
.F...W...R........
..R...F...W...R...
....W...F...R.....
```

## Testing

The project includes unit tests that verify deterministic output and correct resource density. Run them with:

```bash
cargo test
```

## License

MIT Â© ApocalypsAI
