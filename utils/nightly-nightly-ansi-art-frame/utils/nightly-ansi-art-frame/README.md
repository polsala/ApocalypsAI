# nightly-ansi-art-frame

A tiny, self‑contained Python utility that decorates a string with an ASCII/ANSI box.

## Features

- Three built‑in styles: **single**, **double**, and **bold**.
- `auto_style(text)` picks a style deterministically from the input (so the same text always gets the same style).
- Command‑line interface (`python -m utils.nightly-ansi-art-frame.src.frame "Hello"`)
- Zero external dependencies – pure Python 3.11.

## Usage

```bash
python -m utils.nightly-ansi-art-frame.src.frame "Your message here"
```

You can also specify a style explicitly:

```bash
python -m utils.nightly-ansi-art-frame.src.frame "Your message" --style double
```

## Example

```text
+-------------------+
| Hello, world!     |
+-------------------+
```

## Development

Run the test suite with:

```bash
python -m unittest discover utils/nightly-ansi-art-frame/tests
```
