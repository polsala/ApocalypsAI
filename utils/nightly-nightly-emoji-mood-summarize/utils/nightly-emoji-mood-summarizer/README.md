# Nightly Emoji Mood Summarizer

A tiny utility that reads a CSV file of daily mood scores (1-5) and outputs a concise emoji string representing the mood trend.

## How it works

- Input CSV should have two columns: `date` (YYYY-MM-DD) and `mood` (integer 1‑5).
- Each mood value is mapped to an emoji:
  - 5 → 😄
  - 4 → 😊
  - 3 → 😐
  - 2 → 🙁
  - 1 → 😞
- The script prints the emojis in chronological order.

## Usage

```bash
python -m src.mood_summary path/to/mood.csv
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s tests
```
