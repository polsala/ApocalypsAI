# Nightly Docker Quote Server

A whimsical Dockerized Go web service that returns a random quote on each HTTP request.

## Usage

```sh
docker build -t nightly-quote-server .

docker run -p 8080:8080 nightly-quote-server
```

Then visit `http://localhost:8080` to see a random quote.

## How it works

The Go program selects a quote from a hard‑coded list using a time‑based random seed and writes it to the response body.

## Testing

Run the Go tests inside the repository:

```sh
go test ./...
```
