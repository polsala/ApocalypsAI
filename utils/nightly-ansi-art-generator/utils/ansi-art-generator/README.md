# ANSI Art Generator

`ansi-art-generator` is a lightweight, pure‑Python utility that produces random ANSI‑colored block art suitable for terminal display.

## Features

- Generates a rectangular canvas of any size.
- Uses a configurable palette of ANSI colors.
- No external dependencies beyond the Python standard library.
- Includes a simple CLI (`python -m ansi_art_generator`) for quick experimentation.

## Installation

Copy the `utils/ansi-art-generator` folder into your project and import the `generate_art` function:

```python
from ansi_art_generator import generate_art

print(generate_art(width=40, height=10))
```

## CLI Usage

```bash
python -m ansi_art_generator --width 60 --height 15
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/ansi-art-generator/tests
```

## License

MIT © ApocalypsAI
