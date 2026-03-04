# Emoji Portal

A whimsical Dockerized service that returns a random emoji with a short description on each request.

## How it works
The container runs a tiny Flask app exposing a single endpoint:

GET /emoji

The response is JSON, for example:

```
{ "emoji": "🌵", "description": "Desert cactus" }
```

## Build the image
```bash
docker build -t emoji-portal .
```

## Run the container
```bash
docker run -p 8080:8080 emoji-portal
```

## Try it out
```bash
curl http://localhost:8080/emoji
```

## License
MIT
