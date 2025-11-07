# Haiku Generator

A whimsical utility that generates a **deterministic** haiku given an integer seed. Perfect for sprinkling poetic charm into commit messages, PR titles, or just for a quick creative break.

## Installation

```bash
# From the utility folder
cd utils/haiku-generator
pip install .
```

> The utility is self‑contained and has no external runtime dependencies beyond the Python standard library.

## Usage

```bash
python -m src.haiku_generator <seed>
```

Replace `<seed>` with any integer. The same seed will always produce the same haiku.

### Example

```bash
$ python -m src.haiku_generator 42
Silent moonlight glows
Whispers echo through the pine forest
Crimson leaves fall
```

## API

```python
from src.haiku_generator import generate_haiku

haiku = generate_haiku(123)
```

`generate_haiku(seed: int) -> str` returns a three‑line haiku (5‑7‑5 syllable pattern).

## Testing

```bash
pytest -q
```

The test suite lives in `tests/` and runs offline with no network access.
