# nightly-docker-quote-mixer

A whimsical Dockerized HTTP service that returns a randomly mixed quote combining an inspirational phrase with an apocalyptic twist.

## Usage

```sh
docker build -t quote-mixer .
docker run -d -p 8080:8080 --name quote-mixer quote-mixer
curl http://localhost:8080/quote
```

**Sample response**

```json
{
  "quote": "The sun rises, but the shadows whisper."
}
```

## How it works

The Go program picks one line from an internal list of inspirational fragments and one from an apocalyptic fragment list, concatenates them, and serves the result via a tiny HTTP server.

## Tests

Run the test script to build the image, start a container, fetch a quote, and verify the JSON structure:

```sh
bash tests/test_docker.sh
```
