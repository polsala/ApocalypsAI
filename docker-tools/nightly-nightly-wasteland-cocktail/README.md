# nightly‑wasteland‑cocktail

A tiny Docker‑wrapped CLI that spits out a random post‑apocalyptic cocktail recipe.  Perfect for role‑playing sessions, themed parties, or just a good laugh.

## Features

- Generates a cocktail **name**, a list of **ingredients**, and a short **description**.
- Fully containerised – no host‑side dependencies required.
- Deterministic unit tests using mocked randomness.

## Build the image

```bash
docker build -t nightly‑wasteland‑cocktail .
```

## Run the container

```bash
docker run --rm nightly‑wasteland‑cocktail
```

Typical output:

```json
{
  "name": "Radiation‑Ravaged Old‑World Old‑Fashioned",
  "ingredients": [
    "2 oz Mutated Bourbon",
    "1 dash Fallout Bitters",
    "1 tsp Scavenger Sugar Syrup",
    "Orange Peel (charred)"
  ],
  "description": "A smoky reminder of the days before the great fallout. Sip slowly, the world may end any moment."
}
```

## Testing

The repository includes a Python test suite that runs **without internet**.  To execute the tests locally (outside Docker):

```bash
python -m unittest discover -s tests
```

The tests mock the random choices to guarantee deterministic output.
