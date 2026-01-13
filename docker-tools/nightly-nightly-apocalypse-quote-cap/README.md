# Apocalypse Quote Capsule

A tiny Docker container that can **encode** a piece of text (a quote, a message, a secret) into a JSON payload containing the original text, a UTC timestamp and a Base64 representation. It can also **decode** a Base64 string back to the original text.

## Build the image

```sh
docker build -t quote-capsule:latest .
```

## Encode a quote

```sh
echo "The world ends tomorrow" | docker run -i quote-capsule:latest
```

The container will output something like:

```json
{
  "quote": "The world ends tomorrow",
  "timestamp": "2025-12-21T14:32:10Z",
  "encoded": "VGhlIHdvcmxkIGVuZHMgdG9tb3JROW=="
}
```

## Decode a Base64 string

```sh
echo "VGhlIHdvcmxkIGVuZHMgdG9tb3JROW==" | docker run -i quote-capsule:latest --decode
```

Result:

```json
{
  "decoded": "The world ends tomorrow"
}
```

## Testing

The utility ships with a deterministic test suite that mocks Docker commands, so you can run the tests without having Docker installed:

```sh
python -m unittest discover -s tests
```

Enjoy the capsule – keep your post‑apocalyptic messages safe and timestamped!

