# nightly-void-whispers-affirmations

A concurrent Go microservice that delivers whimsical-yet-uplifting affirmations via HTTP.

## Features
- Concurrent request handling
- Lightweight and fast
- JSON response format

## Usage

Start the server:
```bash
go run src/main.go
```

Fetch an affirmation:
```bash
curl http://localhost:8080/affirmation
```

## Example Response

```json
{
  "message": "You are a radiant beacon of possibility in a world of endless wonders."
}
```
