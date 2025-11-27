# Emoji Mood Tracker

Utility that reads lines of text and prefixes each line with an emoji representing the mood (positive 😊, negative 😞, neutral 😐) using a simple keyword‑based sentiment heuristic.

## Usage

```sh
python -m nightly_emoji_mood_tracker.src.mood_tracker [--file <path>]
```

If `--file` is omitted, the utility reads from standard input.

## How it works

- **Positive words**: `happy`, `joy`, `love`, `excellent`, `good`, `great`, `wonderful`, `fantastic`, `awesome`
- **Negative words**: `sad`, `angry`, `hate`, `terrible`, `bad`, `awful`, `horrible`, `worst`
- If a line contains any positive word → 😊, any negative word → 😞, otherwise 😐.

## Testing

Run the test suite with:

```sh
python -m unittest discover utils/nightly-emoji-mood-tracker/tests
```
