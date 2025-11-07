#!/usr/bin/env python3
"""json-palette – colourised JSON pretty printer.

Provides a CLI entry point (`json-palette`) and a small Python API:
    >>> from json_palette import colorize
    >>> print(colorize('{"hello": "world"}'))
"""

import argparse
import json
import sys
from typing import Any

# ANSI colour codes
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
RED = "\033[31m"
RESET = "\033[0m"

def _color_key(key: str) -> str:
    return f"{CYAN}{key}{RESET}"

def _color_str(value: str) -> str:
    return f"{GREEN}\"{value}\"{RESET}"

def _color_num(value: Any) -> str:
    return f"{YELLOW}{value}{RESET}"

def _color_bool(value: bool) -> str:
    return f"{MAGENTA}{value}{RESET}"

def _color_null() -> str:
    return f"{RED}null{RESET}"

def _color_value(val: Any) -> str:
    if isinstance(val, str):
        return _color_str(val)
    if isinstance(val, bool):
        return _color_bool(val)
    if val is None:
        return _color_null()
    if isinstance(val, (int, float)):
        return _color_num(val)
    # For containers we delegate to json.dumps (they will be processed recursively)
    return json.dumps(val)

def _process(obj: Any, indent: int = 0) -> str:
    """Recursively build a colourised JSON string.

    This mirrors `json.dumps(..., indent=4)` but injects colour codes.
    """
    space = " " * indent
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        items = []
        for k, v in obj.items():
            colored_key = _color_key(json.dumps(k))
            colored_val = _process(v, indent + 4)
            items.append(f"{space}    {colored_key}: {colored_val}")
        inner = ",\n".join(items)
        return f"{{\n{inner}\n{space}}}"
    if isinstance(obj, list):
        if not obj:
            return "[]"
        items = [f"{space}    {_process(item, indent + 4)}" for item in obj]
        inner = ",\n".join(items)
        return f"[\n{inner}\n{space}]"
    # Primitive values
    return _color_value(obj)

def colorize(json_input: str) -> str:
    """Return a colourised, pretty‑printed JSON string.

    Parameters
    ----------
    json_input: str
        Raw JSON text.
    """
    try:
        parsed = json.loads(json_input)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc.msg}") from exc
    return _process(parsed)

def _read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main() -> None:
    parser = argparse.ArgumentParser(description="Colourised JSON pretty printer")
    parser.add_argument(
        "source",
        nargs="?",
        default="-",
        help="Path to JSON file or '-' for STDIN (default)"
    )
    args = parser.parse_args()
    raw = _read_input(args.source)
    try:
        coloured = colorize(raw)
    except ValueError as e:
        sys.stderr.write(str(e) + "\n")
        sys.exit(1)
    print(coloured)

if __name__ == "__main__":
    main()
