# Emoji Annotator

`emoji-annotator` is a lightweight, offline Python utility that reads a text file, replaces known keywords with their corresponding emojis, and writes the annotated result to a new file.

## Features
- No network calls – fully deterministic and safe for CI.
- Simple keyword → emoji mapping that can be extended.
- Command‑line interface:
  ```bash
  python -m emoji_annotator <input.txt> <output.txt>
  ```

## Example
```text
I love coffee and cats.
```
Running the annotator produces:
```text
I love ☕ and 🐱.
```

## Installation
The utility is self‑contained; just copy the `src/annotator.py` file and run it with Python 3.11.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/nightly-emoji-annotator/utils/emoji-annotator/tests
```
