# nightly-magic-8-ball

A whimsical Dockerized CLI that answers any question like a Magic 8‑Ball.

## Usage

```bash
docker run --rm ghcr.io/polsala/nightly-magic-8-ball <question>
```

Example:

```bash
docker run --rm ghcr.io/polsala/nightly-magic-8-ball "Will it rain tomorrow?"
```

The container will output a random answer from the classic Magic 8‑Ball responses.

## Building locally

```bash
go build -o magic8ball
docker build -t nightly-magic-8-ball .
```

## Testing

Run the Go tests:

```bash
go test ./...
```
