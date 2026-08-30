# Nightly Survival Quote Service

A tiny Docker‑based HTTP server that returns a daily survival‑themed quote. The quote is deterministic – it is based on the current day of the year (or an optional `DATE_OVERRIDE` environment variable) so tests can be repeatable.

## Build the image
```bash
docker build -t nightly-survival-quote-service .
```

## Run the container
```bash
# Normal mode – uses the host's current date
docker run -d -p 8080:8080 --name quote-service nightly-survival-quote-service

# Test mode – force a specific date for deterministic output
docker run -d -p 8081:8080 -e DATE_OVERRIDE=2023-01-01 --name quote-service-test nightly-survival-quote-service
```

## API
```
GET /quote
```
Returns JSON:
```json
{"quote": "Your quote here"}
```

## Example
```bash
curl http://localhost:8080/quote
```

## Test
The repository includes an automated test script that builds the image, runs a container with a fixed date, queries the endpoint and verifies the response.

```bash
./tests/test_service.sh
```

## License
MIT
