# Nightly Survival Quote API

A tiny Flask web service packaged in a Docker container that returns a whimsical survival‑themed quote.

## How it works
- The service listens on port **5000**.
- `GET /quote` returns a JSON payload with a single quote.
- The quote list is hard‑coded; the first entry is always returned, making the output deterministic for testing.

## Build the image
```bash
docker build -t nightly-survival-quote-api .
```

## Run the container
```bash
docker run -p 5000:5000 nightly-survival-quote-api
```

## Example request
```bash
curl http://localhost:5000/quote
```

Response:
```json
{ "quote": "When the world ends, remember: a well‑stocked pantry is the ultimate weapon." }
```

## Testing
The repository includes a deterministic test suite that uses Flask's test client.
```bash
python -m unittest discover -s tests
```
