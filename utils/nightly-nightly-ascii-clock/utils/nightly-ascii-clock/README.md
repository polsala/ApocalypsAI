# Nightly ASCII Clock

Utility that prints the current local time in a stylized ASCII art representation. Useful for terminal dashboards, scripts, or just for fun.

## Usage

```bash
python -m src.clock
```

or import `get_ascii_time` from `src.clock`.

## Example

```
  |  _   _    
  | |_ . | | |_| 
  |  _|  |_|   |
```

(The output will reflect the actual current time.)

## Tests

Run with `pytest`:

```bash
pytest -q
```
