# Nightly Apocalypse Tip of the Day

A tiny Dockerized utility that prints a whimsical post‑apocalyptic survival tip based on the current date. The tip is deterministic, so running the container on the same day always yields the same tip.

## Usage

```sh
docker build -t tip-of-the-day .
docker run --rm tip-of-the-day
```

## How it works

The container runs a short Python script (`src/tip_of_the_day.py`) that maps the day of year to a tip from a built‑in list. The mapping is deterministic, making it easy to test.

## Adding tips

Edit `src/tip_of_the_day.py` and add new strings to the `TIPS` list.
