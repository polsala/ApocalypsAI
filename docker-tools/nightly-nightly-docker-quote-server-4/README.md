# nightly-docker-quote-server

A minimal Docker‑ized HTTP service that returns a random inspirational quote on each request.

## How it works
- The container runs a tiny Flask app (`app.py`).
- When you hit `GET /` the app selects a random quote from an internal list and returns it as plain text.
- All dependencies are installed in the image, so the container is completely self‑contained.

## Build the image
```bash
docker build -t quote-server .
```

## Run the container
```bash
docker run -p 8080:8080 quote-server
```
The service will be reachable at `http://localhost:8080/`.

## Example request
```bash
curl http://localhost:8080/
# => "The only limit to our realization of tomorrow is our doubts of today."
```

## Testing
The repository includes deterministic unit tests that verify:
- The Dockerfile contains the expected base image and command.
- The Flask app’s helper function returns a quote from the predefined list.

Run the tests with:
```bash
python -m unittest discover -s tests
```
