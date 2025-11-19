# Nightly Emoji Annotator

Utility that adds a random emoji after each sentence in a given text. Great for spicing up logs, messages, or any prose.

## Usage

```bash
python -m src.annotator [--input <file>] [--output <file>]
```

- If `--input` is omitted, reads from **stdin**.
- If `--output` is omitted, writes to **stdout**.

## How it works

The script splits the input text on sentence boundaries (`.`, `!`, `?` followed by whitespace) and appends a randomly chosen emoji from a curated list.

## Testing

Run the test suite with:

```bash
python -m unittest discover -s tests
```
