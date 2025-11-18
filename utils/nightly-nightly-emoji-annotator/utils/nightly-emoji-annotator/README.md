# Nightly Emoji Annotator

**Utility name:** `nightly-emoji-annotator`

## What it does

Scans a plain‑text file line‑by‑line and appends an emoji that reflects the sentiment of the line:

- 😊 for positive lines
- 😞 for negative lines
- 😐 for neutral lines

The sentiment analysis is deliberately lightweight – it relies on a built‑in list of positive and negative keywords.  Users can extend the positive vocabulary at runtime by setting the environment variable `EXTRA_POSITIVE` to a comma‑separated list of words.

## Usage

```bash
python -m utils.nightly-emoji-annotator.src.annotator <input.txt> <output.txt>
```

If no output file is supplied, the annotated text is printed to STDOUT.

## How it works

1. Load the optional `EXTRA_POSITIVE` env var.
2. For each line, count occurrences of positive and negative keywords.
3. Choose the appropriate emoji and append it to the line.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-emoji-annotator/tests
```

---

*This utility is self‑contained, has no external network dependencies, and includes deterministic unit tests.*
