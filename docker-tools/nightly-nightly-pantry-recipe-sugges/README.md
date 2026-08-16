# Nightly Pantry Recipe Suggester

## Overview
`nightly-pantry-recipe-suggester` is a tiny Docker container that helps post‑apocalyptic survivors (or anyone with a sparse pantry) figure out what meals they can whip up from the ingredients they have.

It expects a **CSV file** with two columns:
```
ingredient,quantity
```
- `ingredient` – name of the food item (case‑insensitive).
- `quantity` – a positive integer representing how many units are available.

The container ships with a built‑in, whimsical recipe database (e.g., *Mystic Muesli*, *Radiation‑Free Ramen*, *Scavenger's Stew*). It prints a list of recipes that can be prepared with the supplied inventory.

## Build the image
```bash
docker build -t pantry-suggester .
```

## Run the container
Assuming you have an `inventory.csv` in the current directory:
```bash
docker run --rm -v "$(pwd)/inventory.csv:/data/inventory.csv" pantry-suggester /data/inventory.csv
```
The container will output something like:
```
Possible recipes based on your pantry:
- Mystic Muesli
- Scavenger's Stew
```
If no recipes match, you will see:
```
No recipes can be made with the current inventory.
```

## Development & Testing
The core logic lives in `src/app.py` and is pure Python, making it easy to test locally without Docker.
```bash
python -m unittest discover -s tests
```
All tests are deterministic and use in‑memory CSV data, so no external files or network access are required.

## License
MIT – see the repository LICENSE file.
