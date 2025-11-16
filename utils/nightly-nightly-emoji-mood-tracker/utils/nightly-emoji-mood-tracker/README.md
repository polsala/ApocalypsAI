# Emoji Mood Tracker

A whimsical yet practical utility that lets you record your daily mood as an emoji and view a summary of all recorded moods.

## Features
- Record a mood emoji for the current day.
- Summarize how many times each emoji has been recorded.
- Data is stored locally in a JSON file (`~/.emoji_mood_tracker.json`).

## Installation
The utility is self‑contained Python 3.11 code. No external dependencies are required.

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI
```

## Usage
```bash
# Record a mood (replace 😊 with any emoji you like)
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker record 😊

# Show a summary of all recorded moods
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker summary
```

## Data Location
The moods are persisted in `~/.emoji_mood_tracker.json`. Feel free to inspect or edit this file directly.

## Testing
Run the tests with `pytest`:
```bash
pytest utils/nightly-emoji-mood-tracker/tests
```
