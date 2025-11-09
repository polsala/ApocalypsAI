# Whimsical Compliment Generator

A tiny utility that returns a random whimsical compliment for a given name. Useful for bots, CLI fun, or adding a smile to scripts.

## Usage

```bash
python -m src.compliment "Alice"
# => "Alice, you are a dazzling comet of curiosity!"
```

## API

```python
from src.compliment import get_compliment

msg = get_compliment("Bob")
```

## Testing

Run `python -m unittest discover -s tests` from the utility root.
