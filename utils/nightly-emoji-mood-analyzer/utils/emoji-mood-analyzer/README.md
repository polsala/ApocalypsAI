# Emoji Mood Analyzer

A whimsical‑yet‑useful command‑line utility that scans a short piece of text and returns an emoji representing the detected mood.

## Features
- Pure Python 3.11, no external dependencies.
- Simple keyword‑based mood detection (happy, sad, angry, excited, love, fear, surprised, confused, bored).
- Returns a neutral face (😐) when no mood keyword is found.
- Provides a `main()` entry point so it can be used as a script or imported as a library.

## Installation
Just copy the folder into your repository and run the script with Python:
```bash
python -m utils.emoji-mood-analyzer.src.mood "I am feeling happy today!"
```

## Usage
```text
$ python -m utils.emoji-mood-analyzer.src.mood "I love this project"
❤️
```

## API
```python
from utils.emoji_mood_analyzer.src.mood import analyze_mood

emoji = analyze_mood("I am sad")  # returns "😢"
```

## Testing
The utility ships with a deterministic pytest suite that runs offline. To execute the tests:
```bash
cd utils/emoji-mood-analyzer
pytest -q
```

## License
MIT – see the repository root LICENSE file.
