# Pantry Recipe Suggester

A whimsical Dockerized utility that reads a list of available pantry ingredients and suggests simple recipes you can make with them. No internet required – all recipes are baked into the image.

## Build

```sh
docker build -t pantry-suggester .
```

## Run

Create a file `ingredients.txt` with one ingredient per line, e.g.:

```
bread
cheese
tomato
```

Then run:

```sh
docker run --rm -v "$(pwd)/ingredients.txt":/app/ingredients.txt pantry-suggester
```

The container will output possible recipes.

## How it works

The container runs a tiny Python script that loads a hard‑coded recipe database and matches the supplied ingredients.
