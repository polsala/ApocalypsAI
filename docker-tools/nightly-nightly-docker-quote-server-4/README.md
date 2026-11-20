# nightly-docker-quote-server

A lightweight Docker container that runs a tiny HTTP server exposing a single endpoint `/quote`. The server returns a JSON payload with a quote selected from a built‑in list. The selection is deterministic – you can control which quote is returned by setting the `QUOTE_INDEX` environment variable (default `0`).

## Features
- Zero‑dependency runtime (Alpine Linux + compiled Go binary)
- Deterministic output for reliable CI testing
- Configurable port via `PORT` env var (default `8080`)
- Small image size (~15 MB)

## Build the image
```bash
docker build -t nightly-docker-quote-server .
```

## Run the container
```bash
# Return the first quote (default)
docker run -p 8080:8080 nightly-docker-quote-server

# Return the third quote (index 2)
docker run -e QUOTE_INDEX=2 -p 8080:8080 nightly-docker-quote-server
```

## Example request
```bash
curl http://localhost:8080/quote
```
Response:
```json
{"quote":"The sun rises even in the wasteland."}
```

## Testing
The repository includes a deterministic Bash test that builds the image, runs it with a known `QUOTE_INDEX`, queries the endpoint, and verifies the response.

```bash
cd tests && ./test_main.sh
```

## License
MIT © ApocalypsAI community
