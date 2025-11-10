# Doom Level Assessor

A whimsical utility that evaluates how close a given date is to the fictional apocalypse (2099‑12‑31) and returns a **doom level**:

- `Safe`
- `Warning`
- `Critical`
- `Apocalypse`
- `Already passed`

## Usage

```bash
python -m src.doom 2025-01-01
# → Safe
```

## API

```python
from src.doom import compute_doom_level

level = compute_doom_level("2025-01-01")  # "Safe"
```

The function accepts an ISO‑8601 date string (`YYYY‑MM‑DD`).

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s tests
```
