# Emoji Mood Server

A tiny Go web service that returns an emoji matching a given mood. Containerized with Docker for easy deployment.

## Usage

```sh
docker build -t emoji-mood .
docker run -p 8080:8080 emoji-mood
```

Then request:

```sh
curl "http://localhost:8080/emoji?mood=happy"
# {"emoji":"😊"}
```

## Supported moods

- happy → 😊
- sad → 😢
- angry → 😠
- neutral → 😐
- any other → 🤔

## Testing

```sh
go test ./...
```
