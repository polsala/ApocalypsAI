# Nightly Wasteland Quote Server
A tiny Dockerized Flask service that serves a random post-apocalyptic quote at `/quote`. Perfect for adding a touch of bleak optimism to your micro‑services ecosystem.

## Usage

```sh
docker build -t wasteland-quote .
docker run -p 5000:5000 wasteland-quote
```

Then visit `http://localhost:5000/quote`.

## How it works

The container runs a Flask app (`src/app.py`) that selects a quote from a built‑in list.

## Testing

```sh
python -m pytest tests
```
