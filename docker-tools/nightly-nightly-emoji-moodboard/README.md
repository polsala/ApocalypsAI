# Emoji Moodboard

A tiny Flask web service that returns an emoji representing the current time of day. Perfect for adding a whimsical touch to dashboards or chat bots.

## How it works

- `/mood` endpoint returns JSON `{"emoji":"🌞"}` etc.
- Emoji changes based on hour:
  - 5‑11 → 🌞 (sun)
  - 12‑17 → ☕ (coffee)
  - 18‑21 → 🌙 (moon)
  - 22‑4 → ⭐ (star)

## Running with Docker

```sh
docker build -t emoji-moodboard .

docker run -p 5000:5000 emoji-moodboard
```

Visit `http://localhost:5000/mood`.
