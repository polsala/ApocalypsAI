# ASCII Art Clock

`ascii-art-clock` is a lightweight, zero‑dependency Python utility that renders the current time (or any provided `datetime`) as big ASCII‑art digits.

## Features

- **Instant visual time** – perfect for terminal dashboards, CI logs, or fun scripts.
- **Deterministic rendering** – the same `datetime` always yields the same output.
- **CLI & library usage** – import `render_time` in your code or run the script directly.

## Installation

Copy the `utils/ascii-art-clock/` folder into your repository and run:

```bash
python -m utils.ascii-art-clock.src.clock
```

## Usage

```bash
# Print the current time
python -m utils.ascii-art-clock.src.clock

# Render a specific time (ISO format)
python -m utils.ascii-art-clock.src.clock 2025-12-31T23:59:00
```

## API

```python
from datetime import datetime
from utils.ascii-art-clock.src.clock import render_time

now = datetime.now()
ascii_art = render_time(now)
print(ascii_art)
```

## Testing

Run the bundled tests with `pytest`:

```bash
pytest utils/ascii-art-clock/tests
```
