# Pantry Recipe Suggester

A whimsical Dockerized utility that scans a CSV list of pantry ingredients and suggests simple post‑apocalyptic recipes you can whip up with what you have.

## Usage

```sh
# Prepare a CSV file with one ingredient per line, e.g. pantry.csv
echo "canned beans\nrice\nspice mix" > pantry.csv

# Build the image
docker build -t pantry-suggester .

# Run the container, mounting the CSV into /data
docker run --rm -v "$(pwd)/pantry.csv:/data/pantry.csv" pantry-suggester
```

The container will output recipe suggestions based on the ingredients.

## How it works

The tool contains a tiny hard‑coded recipe database. It matches available ingredients to recipes and prints any that can be made with the supplied pantry.
