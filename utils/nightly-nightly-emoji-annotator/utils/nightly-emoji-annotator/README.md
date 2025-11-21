# Nightly Emoji Annotator

## Overview

`nightly-emoji-annotator` is a lightweight, **offline** Python utility that scans a plain‑text file line‑by‑line and appends an emoji that reflects a very simple sentiment analysis based on keyword matching.

- **Error / failure** → 😱
- **Warning** → ⚠️
- **Success / passed** → 🎉
- No matching keyword → (no emoji)

The tool is self‑contained, has no external dependencies beyond the Python standard library, and ships with deterministic unit tests.

## Usage

```bash
python -m src.annotator <input_file> <output_file>
```

- `<input_file>` – Path to the source text file.
- `<output_file>` – Path where the annotated version will be written.

## Example

**input.txt**
```
Build started
Compilation success
Warning: deprecated API
Tests failed
All done
```

Running the annotator:
```bash
python -m src.annotator input.txt annotated.txt
```

**annotated.txt**
```
Build started
Compilation success 🎉
Warning: deprecated API ⚠️
Tests failed 😱
All done
```

## Implementation Details

- Keyword matching is case‑insensitive.
- Only the first matching keyword per line determines the emoji.
- The script is deliberately simple to keep the utility portable and easy to audit.

## Testing

Run the bundled tests with:
```bash
python -m unittest discover -s tests
```
All tests are deterministic and do **not** perform any network calls.
