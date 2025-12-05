# Nightly Chronicle Keeper Logbook

A simple, command-line utility to record timestamped entries into a Markdown log file. Perfect for documenting daily events, tracking progress, or simply keeping a personal chronicle in the face of... well, everything.

## Usage

```bash
python src/logbook.py "My entry for today. Found a can of beans!"
```

This will append the message, prefixed with the current date and time, to `chronicle.md` in the current directory.

## Configuration

The log file name is hardcoded to `chronicle.md`. Future versions might allow customization.

## Example `chronicle.md`

```markdown
### 2023-10-27 08:30:15
My entry for today. Found a can of beans!

### 2023-10-27 10:45:00
Repaired the leaky roof. It's holding for now.
```

## Development

To run tests:

```bash
python -m unittest tests/test_logbook.py
```
