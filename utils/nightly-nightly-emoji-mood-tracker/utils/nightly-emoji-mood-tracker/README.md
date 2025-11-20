# Nightly Emoji Mood Tracker

## Overview

`nightly-emoji-mood-tracker` is a lightweight command‑line tool that reads a plain‑text file where each line represents a mood (e.g., `happy`, `sad`, `excited`). It aggregates the entries, determines the most frequent mood(s), and prints a friendly emoji‑enhanced summary.

The utility is completely self‑contained, requires only the Python 3.11 standard library, and includes deterministic offline tests.

## Usage

```bash
# Create a sample moods file
cat > moods.txt <<EOF
happy
sad
happy
excited
EOF

# Run the tracker
python -m mood_tracker moods.txt
```

Output example:
```
📈 Mood summary: happy 😊 (2)
```

If multiple moods tie for the top count, all are displayed:
```
📈 Mood summary: happy 😊 (2), sad 😢 (2)
```

## Installation

Simply copy the `utils/nightly-emoji-mood-tracker` directory into your project and run the module with Python 3.11 or later.

## Testing

Run the test suite with:
```bash
python -m pytest utils/nightly-emoji-mood-tracker/tests
```

All tests are offline and use mocks, ensuring deterministic results.
