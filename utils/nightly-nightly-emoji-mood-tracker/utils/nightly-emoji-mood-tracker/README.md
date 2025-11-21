# Nightly Emoji Mood Tracker

Utility that reads a simple mood log file and prints an emoji summary of the day's moods.

## Mood log format

Each line contains a mood keyword, e.g.:

```
happy
sad
excited
neutral
```

Supported moods and emojis:

- `happy` → 😊
- `sad` → 😢
- `excited` → 🤩
- `angry` → 😠
- `neutral` → 😐
- `tired` → 😴

## Usage

```bash
python -m src.mood_tracker path/to/mood.log
```

The script prints a concatenated string of emojis representing the moods, preserving the order defined in the utility.

Example output:

```
😊😊😢
```

## Testing

Run the test suite with:

```bash
pytest -q
```
