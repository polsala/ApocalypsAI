import argparse
import json
import sys
from typing import Any, Dict

# ANSI color codes (simple, no external deps)
_COLOR_RESET = "\033[0m"
_COLOR_KEY = "\033[94m"   # bright blue
_COLOR_STRING = "\033[92m"  # bright green
_COLOR_NUMBER = "\033[93m"  # bright yellow
_COLOR_BOOL = "\033[95m"    # bright magenta
_COLOR_NULL = "\033[90m"    # bright black (gray)


def _colorize(value: Any) -> str:
    """Return a string representation of *value* with optional ANSI colors.

    This function is deliberately simple and only handles the JSON primitive
    types that the standard library's ``json`` module produces.
    """
    if isinstance(value, str):
        return f"{_COLOR_STRING}\"{value}\"{_COLOR_RESET}"
    if isinstance(value, bool):
        return f"{_COLOR_BOOL}{value}{_COLOR_RESET}"
    if value is None:
        return f"{_COLOR_NULL}null{_COLOR_RESET}"
    if isinstance(value, (int, float)):
        return f"{_COLOR_NUMBER}{value}{_COLOR_RESET}"
    # Fallback – should not happen for primitives
    return json.dumps(value)


def _format_json(data: Any, *, indent: int = 2, color: bool = False) -> str:
    """Recursively format *data* into a pretty‑printed JSON string.

    If *color* is ``True`` keys and primitive values are wrapped in ANSI escape
    sequences for terminal highlighting.
    """
    def _dump(obj: Any, level: int) -> str:
        pad = " " * (indent * level)
        if isinstance(obj, dict):
            if not obj:
                return "{}"
            items = []
            for k in sorted(obj.keys()):
                key_repr = f"\"{k}\""
                if color:
                    key_repr = f"{_COLOR_KEY}{key_repr}{_COLOR_RESET}"
                val_repr = _dump(obj[k], level + 1)
                items.append(f"{pad}{' ' * indent}{key_repr}: {val_repr}")
            inner = ",\n".join(items)
            return f"{{\n{inner}\n{pad}}}"
        if isinstance(obj, list):
            if not obj:
                return "[]"
            items = [f"{pad}{' ' * indent}{_dump(item, level + 1)}" for item in obj]
            inner = ",\n".join(items)
            return f"[\n{inner}\n{pad}]"
        # Primitive
        return _colorize(obj) if color else json.dumps(obj)

    return _dump(data, 0)


def _load_json(source: str) -> Dict[str, Any]:
    """Load JSON from *source*.

    *source* can be a file path or ``-`` to indicate STDIN.
    """
    if source == "-":
        raw = sys.stdin.read()
    else:
        with open(source, "r", encoding="utf-8") as f:
            raw = f.read()
    return json.loads(raw)


def main() -> None:
    parser = argparse.ArgumentParser(description="Pretty‑print JSON with sorted keys.")
    parser.add_argument("source", nargs="?", default="-", help="Path to JSON file or '-' for STDIN")
    parser.add_argument("--color", action="store_true", help="Enable ANSI color output")
    args = parser.parse_args()

    try:
        data = _load_json(args.source)
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"Error: Invalid JSON – {exc}\n")
        sys.exit(1)
    except FileNotFoundError:
        sys.stderr.write(f"Error: File not found – {args.source}\n")
        sys.exit(1)

    formatted = _format_json(data, color=args.color)
    print(formatted)


if __name__ == "__main__":
    main()
