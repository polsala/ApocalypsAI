# Nightly Emoji Mood Logger

**Utility name:** `nightly-emoji-mood-logger`

## What it does

`emoji-mood-logger` reads a JSON file containing a list of daily mood entries (date + integer rating 1‑5) and prints a concise, emoji‑rich summary.  The summary shows the average mood per day as a single emoji, making it easy to spot trends at a glance.

## Installation & usage

The utility is pure Python 3.11 and has no external dependencies.

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI

# Navigate to the utility folder
cd utils/nightly-emoji-mood-logger

# Run the logger (example)
python -m src.logger path/to/moods.json
```

## Input format

The input JSON must be an array of objects with the following keys:

```json
[
  {"date": "2025-11-01", "mood": 4},
  {"date": "2025-11-01", "mood": 3},
  {"date": "2025-11-02", "mood": 5}
]
```

- `date` – ISO‑8601 date string (`YYYY‑MM‑DD`).
- `mood` – Integer from **1** (very sad) to **5** (very happy).

## Emoji mapping

| Average mood | Emoji |
|--------------|-------|
| 1‑1.5        | 😢    |
| 1.5‑2.5      | 🙁    |
| 2.5‑3.5      | 😐    |
| 3.5‑4.5      | 🙂    |
| 4.5‑5        | 😄    |

## Example output

```
2025-11-01: 🙂
2025-11-02: 😄
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
