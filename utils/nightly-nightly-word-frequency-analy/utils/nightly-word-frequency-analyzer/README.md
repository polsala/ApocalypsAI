# Nightly Word Frequency Analyzer

Utility that reads a plain‑text file and produces a markdown table of the top N most frequent words.

## Features
- Case‑insensitive word counting.
- Strips common punctuation.
- Configurable `--top` argument (default 10).
- Pure Python 3.11, no external dependencies.

## Usage
```bash
python -m src.analyzer <path-to-text-file> [--top N]
```

The tool prints a markdown table to stdout, e.g.

```markdown
| Word | Count |
|------|-------|
| the  | 42    |
| and  | 37    |
| ...  | ...   |
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s tests
```
