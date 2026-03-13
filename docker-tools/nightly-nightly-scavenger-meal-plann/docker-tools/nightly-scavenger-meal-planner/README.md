# Nightly Scavenger Meal Planner

A whimsical Dockerized utility that reads a list of available pantry items and suggests a post‑apocalypse‑friendly recipe that can be made with those ingredients.

## Usage

```sh
# Prepare a plain‑text file with one ingredient per line, e.g. ingredients.txt
echo -e "canned beans\nspaghetti\ntomato sauce\nwater" > ingredients.txt

# Build the Docker image
docker build -t scavenger-meal-planner ./docker-tools/nightly-scavenger-meal-planner

# Run the planner
docker run --rm -v "$(pwd)/ingredients.txt:/app/ingredients.txt" scavenger-meal-planner
```

The container will output a single recipe suggestion, e.g.:

```
Recipe: Spaghetti with Tomato Sauce and Canned Beans
```

## How it works

The tool contains a tiny built‑in recipe database. It matches recipes whose required ingredients are a subset of the supplied pantry list. If multiple recipes match, one is chosen deterministically using a fixed random seed for reproducibility.

## Testing

Run the unit tests with:

```sh
python -m unittest discover -s docker-tools/nightly-scavenger-meal-planner/tests
```
