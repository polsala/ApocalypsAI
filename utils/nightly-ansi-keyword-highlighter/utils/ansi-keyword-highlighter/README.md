# ANSI Keyword Highlighter

Utility to colorize log messages in the terminal.

## Usage

```bash
python -m ansi_keyword_highlighter "Error: file missing. Warning: low memory. Info: all good."
```

The command prints the input string with the words **Error**, **Warning**, and **Info** colored red, yellow, and green respectively.

## Installation

No external dependencies – just copy the folder and run the script with Python 3.11.

## API

```python
from src.highlighter import highlight

colored = highlight("Error: something went wrong")
```

`highlight(text: str) -> str` returns the input string with the supported keywords wrapped in ANSI escape codes.
