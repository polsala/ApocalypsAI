# Emoji Time Ago

Utility that converts an ISO‑8601 timestamp into a human‑readable relative time description, prefixed with a whimsical emoji (e.g., “🕐 5 minutes ago”). Works offline, pure Python 3.11, no external dependencies.

## Usage

```bash
python -m utils.emoji-time-ago.src.main "2023-01-01T12:00:00Z"
# → 🕐 5 minutes ago
```

## API

```python
time_ago(timestamp: str, now: datetime | None = None) -> str
```

- `timestamp` – ISO‑8601 string (with optional “Z” suffix).
- `now` – optional current time for testing; defaults to `datetime.utcnow()`.

## Tests

Run with `pytest`:

```bash
pytest utils/emoji-time-ago/tests
```
