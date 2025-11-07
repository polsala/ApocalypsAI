# json‑palette

**json‑palette** is a whimsical‑yet‑useful command‑line tool that takes JSON input (from a file or STDIN) and prints it back to the terminal with colourful syntax highlighting.

## Features
- Zero‑dependency Python 3.11 script (only uses the standard library).
- Highlights:
  - **Keys** – cyan
  - **Strings** – green
  - **Numbers** – yellow
  - **Booleans** – magenta
  - **null** – red
- Works with piped input, e.g. `cat data.json | json-palette`.
- Provides a tiny Python API (`json_palette.colorize`) for programmatic use.

## Installation
```bash
# Clone the repository (or copy the utils/json-palette folder) and add it to your PATH
cp -r utils/json-palette /some/dir && export PATH="/some/dir/json-palette:$PATH"
```

## Usage
```bash
# From a file
json-palette data.json

# From a pipe
cat data.json | json-palette
```

## Development
Run the test suite with:
```bash
python -m unittest discover -s utils/json-palette/tests
```

---
*Created by the ApocalypsAI Nightly Integrator.*
