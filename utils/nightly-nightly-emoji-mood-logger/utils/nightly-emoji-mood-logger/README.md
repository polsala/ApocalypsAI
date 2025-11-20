# Nightly Emoji Mood Logger

A whimsical utility that records a timestamped random emoji representing your mood each time it's run. Great for personal logs, team morale dashboards, or just a fun daily habit.

## Features

- Picks a random mood emoji from a curated list.
- Writes an entry `YYYY-MM-DD HH:MM:SS - <emoji>` to a log file.
- CLI usage: `python -m src.logger --output mood.log`
- No external dependencies; works offline.

## Installation

Copy the `utils/nightly-emoji-mood-logger` folder into your repository and run the script with Python 3.11.

## Usage

```sh
python -m src.logger --output my_mood.log
```

## Testing

Run the tests with:

```sh
python -m unittest discover -s tests
```
