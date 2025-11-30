# Emoji Annotator

Utility that scans a text file line by line and appends an emoji that matches detected keywords. Helpful for making logs, notes, or commit messages more expressive.

## Usage

```bash
python -m emoji_annotator.src.annotator <input.txt> <output.txt>
```

The script reads `<input.txt>`, annotates each line, and writes to `<output.txt>`.

## How it works

A small keyword‑to‑emoji map is defined. For each line, the first matching keyword (case‑insensitive) adds its emoji at the end of the line. If no keyword matches, the line is left unchanged.
