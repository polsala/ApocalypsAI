# Nightly Scavenger Meal Planner

A tiny Dockerized utility that reads a list of available pantry items and spits out a whimsical, apocalypse‑themed recipe suggestion. Perfect for when the world is ending and you need to know what to cook with the last cans of beans.

## How it works
1. Provide a plain‑text file `ingredients.txt` (one ingredient per line) and mount it into the container at `/data/ingredients.txt`.
2. Build the Docker image:
   ```bash
   docker build -t scavenger-meal-planner .
   ```
3. Run the container, mounting your ingredient list:
   ```bash
   docker run --rm -v $(pwd)/ingredients.txt:/data/ingredients.txt scavenger-meal-planner
   ```
   The container will print a randomly generated recipe using up to three of the supplied ingredients.

## Example
```text
$ cat ingredients.txt
canned beans
spiced jerky
mystery powder

$ docker run --rm -v $(pwd)/ingredients.txt:/data/ingredients.txt scavenger-meal-planner
🛠️  Radiated Stew with canned beans, spiced jerky, and mystery powder. Enjoy your post‑apocalypse feast!
```

## Determinism for testing
The script seeds the random number generator with a fixed value (`0`) when the `SCAVENGER_TEST_MODE` environment variable is set to `1`. This makes the output deterministic for the automated test suite.

## Files
- `Dockerfile` – builds the container.
- `src/app.py` – core implementation.
- `tests/test_app.py` – unit tests (offline, deterministic).
