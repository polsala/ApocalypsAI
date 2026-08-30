# nightly-docker-quote-server

A whimsical Dockerized HTTP server that serves random apocalypse‑themed quotes.

## Usage

```sh
# Build the image
docker build -t nightly-docker-quote-server .

# Run the container
docker run -d -p 8080:8080 --name quote_server nightly-docker-quote-server

# Get a random quote
curl http://localhost:8080/quote

# Get a deterministic quote (useful for testing)
curl http://localhost:8080/quote?index=0
```

## How it works

The container runs a tiny Flask app (`src/app.py`). The app holds a hard‑coded list of quotes and returns either a random one or the one at the supplied `index`.

## License

MIT
