# nightly-emoji-quote-service

A whimsical Dockerized Flask service that returns a random emoji‑enhanced quote. The quote is deterministic based on an optional `seed` query parameter, making it perfect for testing.

## Usage

```sh
# Build the Docker image
docker build -t emoji-quote .

# Run the container (exposes port 8080)
docker run -p 8080:8080 emoji-quote
```

Then open your browser or use `curl`:

- `http://localhost:8080/quote` – returns a quote based on the current timestamp.
- `http://localhost:8080/quote?seed=42` – returns a deterministic quote for the given seed.

## How it works

The service selects a quote from a short list using `seed % len(quotes)`. If no `seed` is supplied, the current Unix timestamp is used, giving a pseudo‑random experience.

## License

MIT
