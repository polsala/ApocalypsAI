# Emoji Moodboard Docker Utility

Provides a tiny Flask API that returns a moodboard of emojis based on the current hour of the day. Useful for adding a playful status indicator to dashboards or chat bots.

## Build

```sh
docker build -t nightly-emoji-moodboard .
```

## Run

```sh
docker run -p 8080:8080 nightly-emoji-moodboard
```

## API

`GET /mood` returns JSON:

```json
{
  "hour": 14,
  "emoji": ["☀️", "😎"]
}
```

## Testing

```sh
docker run --rm nightly-emoji-moodboard pytest
```
