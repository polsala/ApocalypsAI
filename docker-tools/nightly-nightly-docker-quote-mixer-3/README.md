# nightly-docker-quote-mixer

A whimsical Dockerized microservice that returns a mixed quote combining an inspirational line with an apocalyptic twist. Run the container and query `GET /quote` to receive a JSON payload.

## Usage

```sh
docker build -t quote-mixer .
 docker run -p 8080:8080 quote-mixer
```

Then:

```sh
curl http://localhost:8080/quote
# {"quote":"When the sun rises, the shadows whisper..."}
```

## Implementation

The service is a tiny Flask app (`src/app.py`) that picks a random inspirational quote and a random apocalyptic phrase, concatenates them, and returns JSON.

## Tests

Run `pytest -q` to execute offline tests that mock Docker commands.
