# Quote Mixer Service

A whimsical Dockerized HTTP service that returns a randomly mixed quote combining an inspirational phrase with an apocalyptic twist.

## Usage

```sh
docker build -t quote-mixer .

docker run -p 8080:8080 quote-mixer
```

Then request a quote:

```sh
curl http://localhost:8080/quote
```

Response example:

```json
{"quote":"Reach for the stars — as the world crumbles"}
```

## How it works

The service picks one line from an inspirational list and one from an apocalyptic list, joins them with " — " and returns the result as JSON.

## Testing

Run the Go tests locally (no Docker needed):

```sh
go test ./...
```
