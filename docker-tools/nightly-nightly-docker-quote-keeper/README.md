# nightly-docker-quote-keeper

A whimsical, self‑contained Docker utility that prints a random post‑apocalyptic quote on each execution.

## What it does
- Stores a short list of quirky, survival‑themed quotes.
- When the container starts, it selects one quote at random and prints it to STDOUT.
- No network access required – everything runs locally inside the image.

## Why it’s useful
- Great for a quick morale boost during long terminal sessions.
- Can be used as a fun entrypoint for other containers (e.g., as a health‑check message).
- Demonstrates a minimal, portable Docker workflow without any heavyweight runtime.

## Building the image
```sh
docker build -t quote-keeper .
```

## Running the container
```sh
docker run --rm quote-keeper
```
You should see a random quote, for example:
```
The desert whispers, "Stay hydrated."
```

## Files
- `Dockerfile` – builds a tiny Alpine‑based image.
- `src/entrypoint.sh` – selects and prints a random quote.
- `src/quotes.txt` – the quote database.
- `tests/test_entrypoint.sh` – a deterministic Bash test that ensures the script prints a non‑empty line.

## License
MIT – see the LICENSE file in the repository root.
