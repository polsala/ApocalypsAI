# Nightly Emoji Mood Tracker

A whimsical yet practical command‑line tool that turns numeric mood scores into expressive emojis.

## What it does
- Accepts a JSON file where keys are dates (`YYYY‑MM‑DD`) and values are integer mood scores from **0** (very sad) to **4** (very happy).
- Prints each date followed by the matching emoji, e.g.:
  ```
  2025-11-20 😄
  2025-11-21 😐
  ```
- No external network calls – fully offline.

## Installation & Usage
```bash
# Clone the repo (or let the nightly integrator add this utility)
cd utils/nightly-emoji-mood-tracker
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (none needed beyond stdlib)

# Run the tracker
python -m src.tracker path/to/moods.json
```

## JSON Input Format
```json
{
  "2025-11-20": 4,
  "2025-11-21": 2,
  "2025-11-22": 0
}
```

## Testing
```bash
pytest tests/test_tracker.py
```

## License
MIT – see LICENSE file in the repository root.
