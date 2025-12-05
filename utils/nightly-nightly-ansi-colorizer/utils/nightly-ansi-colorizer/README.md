# nightly-ansi-colorizer

A lightweight, self‑contained Python utility that decorates strings with ANSI escape codes for terminal color and style formatting.

## Features

- **Simple API**: `colorize(text, *styles)` returns the formatted string.
- **Supported styles**: basic foreground colors (`black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`), bright variants (`bright_black`, …), and attributes (`bold`, `underline`, `reverse`).
- **CLI**: `python -m ansi_colorizer "Hello" red bold` prints the styled text.
- **Zero external dependencies** – pure standard‑library Python 3.11.

## Installation

Copy the `utils/nightly-ansi-colorizer` folder into your project or install it as a submodule. No additional packages are required.

## Usage

```python
from ansi_colorizer import colorize

print(colorize("Success!", "green", "bold"))
print(colorize("Warning!", "yellow", "underline"))
```

### CLI Example

```bash
$ python -m ansi_colorizer "Error occurred" red bold
\x1b[31;1mError occurred\x1b[0m
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-ansi-colorizer/tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
