# nightly-void-whispers-affirmations

A lightweight Go service that serves whimsical-yet-helpful affirmations over HTTP.

## Features

- Serves a random affirmation on request
- Lightweight and fast
- Docker-ready

## Usage

Start the server:

```
go run src/main.go
```

Access affirmations:

```
curl http://localhost:8080/affirmation
```

## Example Output

```json
{
  "affirmation": "You are a radiant force of nature, unstoppable in your kindness."
}
```
