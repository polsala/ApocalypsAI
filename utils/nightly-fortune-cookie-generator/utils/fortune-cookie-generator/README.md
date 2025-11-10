# Fortune Cookie Generator

A tiny utility that prints a random fortune cookie message. Whimsical, but can be used for daily inspiration or as a placeholder in scripts.

## Usage

```bash
python -m src.fortune
```

Will output a random fortune.

## How it works

- Contains a static list of classic fortune cookie sayings.
- Uses Python's `random.choice` to select one.
- CLI entrypoint prints the selected fortune.

## Testing

Run `pytest` in the utility folder.
