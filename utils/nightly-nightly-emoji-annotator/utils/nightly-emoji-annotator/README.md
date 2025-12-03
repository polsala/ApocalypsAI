# Nightly Emoji Annotator

Utility that scans input text and inserts emojis next to recognized keywords.

## Usage

```sh
python -m utils.nightly-emoji-annotator.src.emoji_annotator "I love coffee and coding."
```

Outputs:

```
I love ☕ and coding 💻.
```

## How it works

It uses a static mapping of keywords to emojis. No external services are required, making it deterministic and offline.
