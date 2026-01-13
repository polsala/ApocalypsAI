# Apocalypse Safe‑House Generator

A tiny Docker‑based utility that spits out a random ASCII safe‑house layout. Perfect for tabletop games, story‑telling, or just a bit of fun between code reviews.

## Features

- Choose the number of rooms (default: 5)
- Provide a seed for reproducible layouts
- Runs on a minimal Alpine image (≈5 MB)

## Usage

```bash
# Build the image (only needed once)
docker build -t safehouse-generator .

# Run with defaults (5 rooms, random seed)
docker run --rm safehouse-generator

# Specify number of rooms
docker run --rm safehouse-generator --rooms 8

# Reproducible layout with a seed
docker run --rm safehouse-generator --rooms 4 --seed 12345
```

The output looks like:

````
+----------------------+
| Room 1 | Room 2 | ...|
+----------------------+
| ...                 |
+----------------------+
````

## Development

The generator is a single Bash script (`src/generate.sh`).

### Run locally without Docker

```bash
chmod +x src/generate.sh
./src/generate.sh --rooms 3 --seed 42
```

### Tests

```bash
chmod +x tests/test_generate.sh
./tests/test_generate.sh
```

## License

MIT – see LICENSE file in the repository.
