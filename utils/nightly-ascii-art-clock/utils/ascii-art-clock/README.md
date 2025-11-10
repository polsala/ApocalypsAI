# ASCII Art Clock

A tiny utility that prints the current time in big ASCII‑art digits.

## Features

* No external dependencies – pure Python 3.11.
* Works offline; perfect for scripts, terminal dashboards, or fun demos.
* Deterministic rendering – each digit is rendered the same way every run.

## Usage

```sh
python -m ascii_art_clock
```

Or import the `render_time` function:

```python
from ascii_art_clock import render_time
import datetime
print(render_time(datetime.datetime.now().time()))
```

## How it works

The utility maps each character (`0‑9` and `:`) to a three‑line ASCII pattern and stitches them together for the `HH:MM` format.

## Testing

Run the bundled tests with:

```sh
python -m unittest discover -s utils/ascii-art-clock/tests
```
